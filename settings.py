
EMOJI = [
	":negative_squared_cross_mark:",
	":green_square:",
	":o2:",
	":sos:"
]

NUMBER = [
	1,
	0,
	-1,
	2
]

EMOJI_NUMBER = {emoji: NUMBER[idx] for idx, emoji in enumerate(EMOJI)}
NUMBER_EMOJI = {number: EMOJI[idx] for idx, number in enumerate(NUMBER)}

LIKE_EMOJI = ["👍","👎"]