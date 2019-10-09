name = "Test Debug Placeholder Site Name"
manga = {"author1": ["manga1", "manga2", "manga3"],
		"author2": ["manga4", "manga5"]}
async def get_manga_by_author(author):
	if author in manga:
		return manga[author]
	else:
		return []

