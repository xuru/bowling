

docs:
	cd docs && make html && open build/html/index.html

clean:
	find . -type f \( -iname "*.o" -o -iname "*.obj" -o -iname "*.pyo" -o -iname "*.pyc" -o -iname "*[~]" \) -exec rm -vf {} \;

db:
	python -c "from app import db; db.create_all()"

serve:
	python -c "from app import app; app.run(debug=True)"

demo:
	python demo.py

test:
	nosetests -s tests
