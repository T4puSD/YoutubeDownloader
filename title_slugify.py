class TitleSlugify:
	def __init__(self):
		self.unsafe_chars=['\\','/',':','?','"','<','>','|']

	def slugify_for_windows(self,title):
		unsafe_found = [c for c in title if c in self.unsafe_chars]
		for i in unsafe_found:
			title = title.replace(i,'-')
		# title = u'_'.join(title.split)
		return title

if __name__ == "__main__":
	titleSluggify = TitleSlugify()
	new_title = titleSluggify.slugify_for_windows(r'Tujhe \ Kitna Chahein Aur Hum | Kabir Singh | Jubin Nautiyal Live | Mithoon | Thomso 2019 | IIT Roorke.mp4')
	print(new_title)
	assert new_title == 'Tujhe - Kitna Chahein Aur Hum - Kabir Singh - Jubin Nautiyal Live - Mithoon - Thomso 2019 - IIT Roorke.mp4'