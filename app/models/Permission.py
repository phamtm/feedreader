class Permission:
	"""
	Application permissisons
	Task name 			Bit values 			Description
	Follow 				0b00000001 (0x01)
	Comment 			0b00000010 (0x02)
	Write articles 		0b00000100 (0x04)
	Moderate comments 	0b00001000 (0x08)
	Admin access 		0b10000000 (0x80) 	Administrative access to this site
	"""
	FOLLOW 				= 0x01
	COMMENT 			= 0x02
	WRITE_ARTICLES 		= 0x04
	MODERATE_COMMENTS 	= 0x08
	ADMIN 				= 0x80

roles = {
	'user': (
		Permission.FOLLOW |
		Permission.COMMENT |
		Permission.WRITE_ARTICLES,
		True
	),
	'moderator': (
		Permission.FOLLOW |
		Permission.COMMENT |
		Permission.WRITE_ARTICLES |
		Permission.MODERATE_COMMENTS,
		False
	),
	'admin': (
		0xff,
		False
	)
}