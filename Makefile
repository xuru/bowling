

docs:
	cd docs && make html && open build/html/index.html

clean:
	find . -type f \( -iname "*.o" -o -iname "*.obj" -o -iname "*.pyo" -o -iname "*.pyc" -o -iname "*[~]" \) -exec rm -vf {} \;

serve:
	python run.py

demo:
	python demo.py

test:
	nosetests -s tests
