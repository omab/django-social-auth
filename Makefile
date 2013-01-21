doc-tar:
	tar -czvf doc-example.tar.gz example/ doc/

rpm: doc-tar
	rpmbuild --define "_topdir  %(pwd)" \
	--define "_builddir /tmp" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir  %{_topdir}" \
	-ba django-social-auth.spec

	mv noarch/*.rpm .

test:
	rpmlint -i *.rpm *.spec

clean:
	rm -rf noarch/ BUILDROOT/
	rm -f doc-example.tar.gz

distclean: clean
	rm -f *.rpm

help:
	@echo "Usage: make <target>                                    "
	@echo "                                                        "
	@echo " doc-tar - create tarball with docs and example for RPM "
	@echo " rpm - create rpm package                               "
	@echo " test - test all packages/spec files with rpmlint       "
	@echo " clean - clean files used to build                      "
	@echo " distclean - execute clean and remove all output files  "
	@echo " help - show this help and exit                         "
