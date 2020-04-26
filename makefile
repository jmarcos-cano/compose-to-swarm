deploy: git
	@python3 -m mkdocs gh-deploy

git:
	@git add . || true
	@git commit -m "auto deploy" || true
	@git push origin master || true

serve:
	@python3 -m mkdocs serve
s: serve