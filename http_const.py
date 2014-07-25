HTTP_OK						= 200	# The request completed successfully

HTTP_CREATED				= 201	# The request completed successfully and a
									# new resource was created as a result

HTTP_REDIRECT 				= 302   # A redirect request was issued

HTTP_BAD_REQUEST            = 400   # The request is invalid or inconsistent

HTTP_UNAUTHORIZED           = 401   # The request does not include 
                                    # authentication information

HTTP_FORBIDDEN 				= 403   # The authentication credentials sent with 
                                    # the request are insufficient for the 
                                    # request

HTTP_NOT_FOUND 				= 404   # The resource referenced in the URL was 
                                    # not found

HTTP_INTERNAL_SERVER_ERROR 	= 500   # An unexpected error has occurred while
                                    # processing the request
