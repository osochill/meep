from Cookie import SimpleCookie

def set_cookie(name, value, path='/'):
	cookie = SimpleCookie()
	cookie[name] = value
	cookie[name]['path'] = path
	
	