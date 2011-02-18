PYTHON=`which python`

all:
	@echo "To install py-xsp, run 'make install'."

install: 
	$(PYTHON) install.py

clean:
	rm -f *.pyc
	rm -f *~
