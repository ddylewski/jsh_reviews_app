# User homepage view
from django.shortcuts import render

def home(request):
	return render(request, 'home.html')

# Add these imports at the top
import requests
from django.http import JsonResponse

# ... your other views might be here ...

def lookup_isbn(request):
	"""
	An API view that looks up a book by its ISBN using the Google Books API.
	Returns data compatible with the Book model fields.
	"""
	isbn = request.GET.get('isbn')
	if not isbn:
		return JsonResponse({'error': 'ISBN parameter is missing'}, status=400)

	# The Google Books API endpoint for ISBN lookup
	api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

	try:
		response = requests.get(api_url)
		response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
		data = response.json()

		if data.get('totalItems', 0) == 0:
			return JsonResponse({'error': 'Book not found for this ISBN'}, status=404)

		# Extract the relevant information
		volume_info = data['items'][0]['volumeInfo']

		# The API returns authors as a list, so we join them
		authors = ", ".join(volume_info.get('authors', ['Unknown Author']))
		publisher = volume_info.get('publisher', 'Unknown Publisher')
		published_date = volume_info.get('publishedDate', '')
		publication_year = int(published_date.split('-')[0]) if published_date and published_date.split('-')[0].isdigit() else 1900

		# Book model expects author_name and author_institution (institution not available from API)
		book_data = {
			'title': volume_info.get('title', ''),
			'isbn': isbn,
			'publisher': publisher,
			'publication_year': publication_year,
			'author_name': authors,
			'author_institution': '',  # Not available from Google Books API
		}

		return JsonResponse(book_data)

	except requests.exceptions.RequestException as e:
		return JsonResponse({'error': str(e)}, status=500)
