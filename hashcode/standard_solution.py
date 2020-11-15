#first thing to do is construct a reader that takes the list and spits out a list of object
class Signer():
	"""this is an administrative object, it looks all over the signung process,
	 it stores books score, total scan days and directory of books scanned
	 will add some functions here"""
	def __init__(self, total_books, num_libaries,days_for_scanning, books_scores):
		self.total_books =  total_books
		self.num_libaries = num_libaries
		self.days_for_scanning = days_for_scanning
		self.books_scores =   books_scores
		self.book_directory = []
		
class Libary():
	"""class template for each libaries
	object will contain books, sign time, books it can scan per day
	and unique books i.e books not scanned by libaries """
	def __init__(self,id_number, books, sign_time, shipped_books_per_day):
		self.id_number = id_number
		self.books = books
		self.sign_time = sign_time
		self.shipped_books_per_day = shipped_books_per_day
		self.total_time = (len(books)/int(shipped_books_per_day)) + int(sign_time)
		self.total_score = 0
		self.value_per_time = 0
		self.unique_books = []
	def scoring(self,signer):
		total_score = 0
		for i in self.books:
			total_score += int(signer.books_scores[int(i)])
		return total_score
	def find_unique_books(self,signer):
		flagged_books = set(self.books).intersection(set(signer.book_directory))
		for i in self.books:
			if i not in flagged_books:
				self.unique_books.append(i)
				signer.book_directory.append(i)
		
def reader(file):
	#reads and return contents of files
	"""it returns all libaries details and the libary books themselves"""
	with open(file) as f:
		contents = f.readlines()
		libary_details = contents[:2]
		libaries = contents[2:]
		return libaries,libary_details

file = "a_example.txt"#input file url here
file_b = "b_read_on.txt"
file_f = "f_libraries_of_the_world.txt"
libaries , libary_details = reader(file_f)
books_scores = libary_details[1].split()#scores of all the books, to be stored in the signer object
libary_details = libary_details[0].split()#details of libaries to be stored in the signer object
signer = Signer(libary_details[0],libary_details[1],libary_details[2],books_scores)
libaries = [i.split() for i in libaries]
l_details = libaries[0:len(libaries):2]
l_books = libaries[1:len(libaries):2]
libaries = []
for i in range(len(l_details[:-1])):
	libaries.append(Libary(i,l_books[i],l_details[i][1],l_details[i][2]))
for i in libaries:
	i.total_score = i.scoring(signer)
	i.value_per_time =i.total_score/i.total_time

val_per_time_list = [i.value_per_time for i in libaries]
libaries_id = [i.id_number for i in libaries]
val_per_time_list, libaries_id = (list(t) for t in zip(*sorted(zip(val_per_time_list, libaries_id), reverse = True)))
for i in libaries:
	i.find_unique_books(signer)

with open("_solution.txt",'w') as file:
	file.write(f'{len(libaries_id)}\n')
	for i in libaries_id:
		file.write(f"{i} ")
		for j in libaries:
			if j.id_number == i:
				file.write(f"{len(j.unique_books)}\n")
				for book in j.unique_books:
					file.write(f"{book} ")
				file.write("\n")
print(len(libaries_id))