

clean:
	find . -type f \( -iname "*.o" -o -iname "*.obj" -o -iname "*.pyo" -o -iname "*.pyc" -o -iname "*[~]" \) -exec rm -vf {} \;

test:
	nosetests -s tests
