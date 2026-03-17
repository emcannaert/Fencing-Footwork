import pyttsx3
import argparse
import time
import random 
from datetime import datetime

def read_lesson(file_path):
	# Initialize the TTS engine
	engine = pyttsx3.init()

	voices = engine.getProperty('voices')
	#engine.setProperty('voice', voices[64].id)
	#engine.setProperty('rate', 100)
	try:
		# Open and read the text file
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.readlines()

		for line in content:
			line_splt = line.split()
			if len(line_splt) == 0: continue
			if line_splt[0] == "pause":
				engine.runAndWait()
				time.sleep(float(line_splt[1]))
			else:
				print("saying %s"%line.strip())
				engine.say(line.strip())
		engine.runAndWait()

	except FileNotFoundError:
		print(f"Error: The file at {file_path} was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")


# returns the advance length, retreat length, long retreat length, and lunge lengths 
# for different fencer classes in feet

def get_fencer_pars(fencerType):
	if fencerType == "child":
		return 0.7, -1.0, -1.3, 1.8
	elif fencerType == "normal":
		return 1.0, -1.2, -1.6, 2.0
	elif fencerType == "athletic":
		return 1.2, -1.5, -1.9, 2.3
	else:
		raise ValueError("ERROR: Incorrect fencer type: %s"%fencerType)


# return the tempi (= time to complete) for each different action (advance, retreat, long retreat, lunge) in seconds
def get_action_tempi(pace):
	if pace == 1:
			   # advance  retreat  long-retreat  lunge    fleche? adv-lunge? retr-lunge? long-lunge?
		return     3.0,     3.0,       3.0,        5.0
	elif pace == 2:
		return     2.2,     2.2,       2.2,        3.0
	elif pace == 3:
		return     1.8,     1.8,       1.8,        2.5
	elif pace == 4:
		return     1.0,     1.0,       1.0,        1.8
	elif pace == 5:
		return     0.8,     0.8,       0.8,       1.5

# return the action frequency (= probability of certain actions). Advance = 0, retreat = 1, long retreat = 2, lunge = 3
def get_rand_action():

		rand_action = random.random()

		adv_f 	   = 0.45
		ret_f 	   = adv_f + 0.35
		long_ret_f = ret_f + 0.10
		lunge_f	   = long_ret_f + 0.10


		if rand_action <= adv_f:
			return 0
		elif rand_action > adv_f and rand_action <= ret_f:
			return 1
		elif rand_action > ret_f and rand_action <= long_ret_f:
			return 2
		elif rand_action > long_ret_f and rand_action < lunge_f:
			return 3
		else:
			raise ValueError("ERROR: invalid random number: %s"%rand_action)
 
def isValidAction(action_len, pos, piste_length, end_margin):
	# does this put the 
	if ( (pos + action_len) < (piste_length - end_margin) and (pos + action_len) > (end_margin) ): return True
	else: return False


def create_lesson(fencerType, time_left, pace, piste_length, end_margin, outfile_str):

	action_lens	 = get_fencer_pars(fencerType)
	action_ts    = get_action_tempi(pace)

	pos = piste_length / 2.0

	actions = ["advance", "retreat", "long retreat", "lunge"]


	# create the lesson plan text file
	with open("test%s.txt" % outfile_str, "w") as lesson:

		lesson.write("Hey, kids\n")
		lesson.write("Welcome to Uncle Scott's torture chamber: %s seconds in hell\n"%(time_left))
		lesson.write("Let's get started in five\n")
		lesson.write("pause 1\n")
		lesson.write("four\n")
		lesson.write("pause 1\n")
		lesson.write("three\n")
		lesson.write("pause 1\n")
		lesson.write("two\n")
		lesson.write("pause 1\n")
		lesson.write("one\n")
		lesson.write("pause 1\n")

		while time_left > 0:
			valid_action = False
			action = None
			while not valid_action:
				# generate a random action
				action 		  = get_rand_action()
				valid_action  = isValidAction(action_lens[action], pos, piste_length, end_margin)
			if action in list(range(4)):
				lesson.write("%s\n"%(actions[action]))
				lesson.write("pause %s\n"%(action_ts[action]))
			else:
				raise ValueError("ERROR: no valid action determined.")

			time_left -= action_ts[action]
			pos 	  += action_lens[action]
			if pos < 0 or pos > piste_length:
				raise ValueError("ERROR: fencer position is off the piste.")

		lesson.write("Lesson complete.\n")
		lesson.write("Well done.\n")

	return
	
if __name__=="__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--infile", help="Input File path")
	parser.add_argument("--fencerType", required=True, help="Fencer type of the user(s). Options: child, normal, athletic")
	parser.add_argument("--pisteLength", type=int, required=True, help="Length of the piste being used (in feet)")
	parser.add_argument("--duration", type=int, required=False, default = 60, help="Duration of exercise (in seconds)")
	parser.add_argument("--pace", type=int, required=False, default = 2, help="Pace setting that determines speed of actions (1-5, default is 2)")
	parser.add_argument("--endMargin", type=int, required=False, default = 8, help="How far from the start or end of the piste to start moving backwards (in feet).")
	parser.add_argument("--saveExercise", required=False, action='store_true', help="Save the exercise itinerary.")

	args = parser.parse_args()

	engine = pyttsx3.init()
	voices = engine.getProperty('voices')

	#for index, voice in enumerate(voices):
	#	print(f"Index: {index} | Name: {voice.name} | Languages: {voice.languages}")

	fencerType = args.fencerType.lower()

	if fencerType not in ["child", "normal", "athletic"]:
		raise ValueError("ERROR: fencerType %s is not one of the accepted options: child, normal, athletic"%(fencerType))
	if args.pace > 5 or args.pace < 1: 
		raise ValueError("ERROR: pace setting %s is not in the acceptable range (1-5)."%args.pace)

	infile = "test.txt"

	outfile_str = ""
	if args.saveExercise:
		now = datetime.now()
		outfile_str = now.strftime("_%d-%m-%Y %H:%M:%S")
		infile = "test%s.txt"%outfile_str
	if args.infile: infile = args.infile
	else:	create_lesson(fencerType, args.duration,args.pace, args.pisteLength, args.endMargin, outfile_str)


	# create lesson plan for x minutes
	read_lesson(infile)


	### vary the sleep timing
	### make combo moves 



