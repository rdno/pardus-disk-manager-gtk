all:
	echo "make (tags | clean)"
tags:
	etags *.py disk_manager_gtk/*.py
clean:
	find . -name *~ | xargs rm -rf
	find . -name *.pyc | xargs rm -rf
