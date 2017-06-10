run:
	(cd alpha_beta_iota; DEBUG=1 python manage.py runserver 0:4000)

static:
	(cd alpha_beta_iota; DEBUG=1 python manage.py collectstatic)

manage:
	(cd alpha_beta_iota; DEBUG=1 python manage.py $(filter-out $@,$(MAKECMDGOALS)))

install:
	pip install $(filter-out $@,$(MAKECMDGOALS))
	pip freeze >requirements.txt
