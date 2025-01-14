class Utils:    
    @staticmethod
    def get_item_type(category_type):
        return 'task' if category_type == 'todo_list' else 'item'

import requests

class ApiRequest:

    @staticmethod
    def search_movies(base_url, query):
        url = base_url + "?query={}".format(query)
        headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5ZWU3ZWM2NTQwZTMyNzE0N2U5NTFkNmYxNmQ1YzZiMiIsIm5iZiI6MTczNjI3NDYzNS45MzI5OTk4LCJzdWIiOiI2NzdkNzJjYjgxN2QzNTZhMWE3MjZiYzciLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.A3a4QbmFwCAPRgCLmVDFWW3XvUfiMfiPm8YYk2MsXRQ'
        }

        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            results = json_data.get('results', json_data)
            limited_results = results[:5]
            results = []
            
            for current_movie in limited_results:
                print(current_movie)
                result = {}
                result['api_id'] = current_movie.get('id')
                result['title'] = ApiRequest.format_title(current_movie.get('title'), current_movie.get('original_title'))
                result['description'] = current_movie.get('overview')
                result['image'] = "https://image.tmdb.org/t/p/w500" + str(current_movie.get('poster_path'))
                result['grade'] = current_movie.get('vote_average')
                result['release_year'] = ApiRequest.format_release_date(current_movie.get('release_date'))
                results.append(result)
            return results
        return []

    @staticmethod
    def search_games(base_url, query):
        return []

    @staticmethod
    def get_api_search(base_url, query, category_type):
        search_methods = {
            'movie': ApiRequest.search_movies,
            # 'game': ApiRequest.search_games,
        }
        
        search_method = search_methods.get(category_type)
        if search_method:
            return search_method(base_url, query)
        return []

    @staticmethod
    def format_release_date(date_str):
        if not date_str:
            return "Unknown"
        try:
            return date_str.split('-')[0]
        except ValueError:
            return date_str

    @staticmethod
    def format_title(title, original_title):
        formated_title = title
        if original_title and original_title != title:
            formated_title = f"{title} ({original_title})"
        return formated_title


        # {'adult': False, 'backdrop_path': '/XuvGhhRp3DqpSrD5b0QS1d6CW0.jpg', 'genre_ids': [27, 18], 'id': 135195, 'original_language': 'th', 'original_title': 'P', 'overview': 'An orphan girl taught magic by her sick grandma must find work in seedy Bangkok, where she encounters a number of unsavory characters. She uses the magical skills her grandmother taught her to her advantage and to increasingly horrific consequences.', 'popularity': 8.593, 'poster_path': '/z5CtmnbGyek9Yv40YecPlHXpy3z.jpg', 'release_date': '2005-10-07', 'title': 'P', 'video': False, 'vote_average': 5.843, 'vote_count': 89}