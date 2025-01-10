import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
	def __init__(self, m1_ena, m1_in1, m1_in2, m2_in1, m2_in2, m2_ena):
		self.m1_ena = m1_ena
		self.m1_in1 = m1_in1
		self.m1_in2 = m1_in2
		
		self.m2_ena = m2_ena
		self.m2_in1 = m2_in1
		self.m2_in2 = m2_in2

		GPIO.setup(self.m1_ena, GPIO.OUT)
		GPIO.setup(self.m1_in1, GPIO.OUT)
		GPIO.setup(self.m1_in2, GPIO.OUT)
		
		GPIO.setup(self.m2_ena, GPIO.OUT)
		GPIO.setup(self.m2_in1, GPIO.OUT)
		GPIO.setup(self.m2_in2, GPIO.OUT)
		
		self.m1_pwm = GPIO.PWM(self.m1_ena, 100)
		self.m2_pwm = GPIO.PWM(self.m2_ena, 100)
		self.m1_pwm.start(0)
		self.m2_pwm.start(0)


	def move(self, speed=1, trun=0, t=0):
		speed *=100
		trun *=100
		leftSpeed = speed - trun
		rightSpeed = speed + trun

		if leftSpeed>100: leftSpeed=100
		elif leftSpeed<-100:leftSpeed=-100
		if rightSpeed>100: rightSpeed=100
		elif rightSpeed<-100: rightSpeed=-100
		
		print(abs(leftSpeed), abs(rightSpeed))


		self.m1_pwm.ChangeDutyCycle(abs(leftSpeed))
		self.m2_pwm.ChangeDutyCycle(abs(rightSpeed))
		
		if leftSpeed>0: 
			GPIO.output(self.m1_in1, GPIO.LOW)
			GPIO.output(self.m1_in2, GPIO.HIGH)
		else: 
			GPIO.output(self.m1_in1, GPIO.HIGH)
			GPIO.output(self.m1_in2, GPIO.LOW)

		if rightSpeed>0:
			GPIO.output(self.m2_in1, GPIO.LOW)
			GPIO.output(self.m2_in2, GPIO.HIGH)
		else:
			GPIO.output(self.m2_in1, GPIO.HIGH)
			GPIO.output(self.m2_in2, GPIO.LOW)
			
		sleep(t)

	def stop(self, t=0):
		GPIO.output(self.m1_in1, GPIO.LOW)
		GPIO.output(self.m1_in2, GPIO.LOW)
		GPIO.output(self.m2_in1, GPIO.LOW)
		GPIO.output(self.m2_in2, GPIO.LOW)
		self.m1_pwm.ChangeDutyCycle(0)
		self.m2_pwm.ChangeDutyCycle(0)
		sleep(t)

def main():
	motor = Motor(13,5,6, 17, 27,12) #Motor(12,3,4, 17,27,13)
	
	motor.move(-0.8,0,1) 
	motor.stop(2)

if __name__ == '__main__':
	main()
