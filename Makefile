# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* aiworkout/*.py

black:
	@black scripts/* aiworkout/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr aiworkout-*.dist-info
	@rm -fr aiworkout.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# path of the file to upload to gcp (the path of the file should be absolute or should match the directory where the make command is run)
LOCAL_PATH="data"

# project id
PROJECT_ID=compact-voyager-348405

# bucket name
BUCKET_NAME="aiworkout"

# bucket directory in which to store the uploaded file (we choose to name this data as a convention)
BUCKET_FOLDER=data

# name for the uploaded file inside the bucket folder (here we choose to keep the name of the uploaded file)
# BUCKET_FILE_NAME=another_file_name_if_I_so_desire.csv
BUCKET_FILE_NAME=$(shell basename ${LOCAL_PATH})

REGION=us-east1

set_project:
	-@gcloud config set project ${PROJECT_ID}

create_bucket:
	-@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

upload_data:
	-@gsutil cp ${LOCAL_PATH} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME}

# will store the packages uploaded to GCP for the training
BUCKET_TRAINING_FOLDER = 'trainings'

##### Machine configuration - - - - - - - - - - - - - - - -

PYTHON_VERSION=3.7
FRAMEWORK=scikit-learn
RUNTIME_VERSION=2.2

##### Package params  - - - - - - - - - - - - - - - - - - -

PACKAGE_NAME=aiworkout
FILENAME=find_angle  ######change this when we know the filename

##### Job - - - - - - - - - - - - - - - - - - - - - - - - -

# JOB_NAME=aiworkout_training_pipeline_$(shell date +'%Y%m%d_%H%M%S')

run_locally:
	@python -m ${PACKAGE_NAME}.${FILENAME}

# gcp_submit_training:
# 	gcloud ai-platform jobs submit training ${JOB_NAME} \
# 		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
# 		--package-path ${PACKAGE_NAME} \
# 		--module-name ${PACKAGE_NAME}.${FILENAME} \
# 		--python-version=${PYTHON_VERSION} \
# 		--runtime-version=${RUNTIME_VERSION} \
# 		--region ${REGION} \
# 		--stream-logs

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ __pycache__
	@rm -fr build dist *.dist-info *.egg-info
	@rm -fr */*.pyc


##### Prediction API - - - - - - - - - - - - - - - - - - - - - - - - -

run_api:
	uvicorn api.fast:app --reload
# load web server with code autoreload

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1
