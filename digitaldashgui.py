import cv2
import numpy as np
import random
import time

warnings_found = 0 #no warnings found
warnings_displayed = 0 #no warnings displayed
dashboard = np.zeros((400,800,3))

x,y = (0,0) #dashboard initial position

scale = 50
w,h = (int(dashboard.shape[1] * scale/100),int(dashboard.shape[0]*scale/100))

def draw_arc(center,radius,startangle,endangle,color,thickness,text,subtextUP='',subtextDOWN=''): #counterclockwise angle negative
	axes = (radius,radius)
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontscale = radius/40
	linetype = 3
	
	text_sizea = cv2.getTextSize(text,font,fontscale,linetype)
	subtextUP_size = cv2.getTextSize(subtextUP,font,1,1)
	subtextDOWN_size = cv2.getTextSize(subtextDOWN,font,1,1)
	#print(text_sizea)
	tx,ty = center
	angle = 0
	displayat = ((tx-(text_sizea[0][0])/2),(ty+(text_sizea[0][1])/2)) #centering text
	tt=1
	if radius <= 100:
		tt=2
	subtextUPat = ((tx-(subtextUP_size[0][0])/tt),(ty+2*subtextUP_size[1]-(radius+subtextUP_size[0][1])/2))
	subtextDOWNat = ((tx-(subtextDOWN_size[0][0])/tt),(ty+2*subtextDOWN_size[1]+(radius-subtextDOWN_size[0][1])/2))
	fontcolor = (255,255,255)

	#merge text with img
	cv2.ellipse(dashboard,center,axes,angle,startangle,endangle,color,thickness)
	cv2.putText(dashboard,text,displayat,font,fontscale,fontcolor,linetype)
	cv2.putText(dashboard,subtextUP,subtextUPat,font,radius/70,fontcolor,radius/50)
	cv2.putText(dashboard,subtextDOWN,subtextDOWNat,font,radius/70,fontcolor,radius/50)

	#display small text below
	return ((tx,ty),radius,text_sizea,displayat,(fontscale,fontcolor,linetype),center,startangle,endangle,color,thickness,angle,subtextUP,subtextDOWN)


def overlay_image(src, overlay, posx, posy,S,D):  #for overlaying blank image at (x,y) wth blend (g,r,b)
	srcheight, srcwidth, srcchannels = src.shape
	overlayheight, overlaywidth, overlaychannels = overlay.shape
	for x in range(overlaywidth):
		if x+posx < srcwidth:
			for y in range(overlayheight):
				if y+posy < srcwidth:
					source = src[y+posy,x+posx] 
					over   = overlay[y,x] 
					merger = [0, 0, 0, 0]

					for i in range(2):
						merger[i] = (S[i]*source[i]+D[i]*over[i])

					src[y+posy,x+posx,1] = merger[0]
					src[y+posy,x+posx,2] = merger[1]
					src[y+posy,x+posx,0] = merger[2]




def update_arc(arc_data,text):
	cv2.circle(dashboard,arc_data[5],arc_data[1],(0,0,0),-1) #draw black filled circle
	draw_arc(arc_data[5],arc_data[1],arc_data[6],arc_data[7],arc_data[8],arc_data[9],text,subtextUP=arc_data[11],subtextDOWN=arc_data[12]) #update data

def update_warning_symbols():
	#blank jpg
	blank = np.zeros((50,50,3))

	#collect warning symbols from png file
	brake = cv2.imread('brake.png')
	seatbelt = cv2.imread('seatbelt.png')
	batterytemp = cv2.imread('battery_temp.jpg')
	batterylow = cv2.imread('batt_low_warning.png')
	tyrepressure = cv2.imread('tyre_pressure.png')

	#set position of warning coordinates
	sx,sy = (x+20,y+300)
	fx,fy = (sx+200,sy+300)
	brakex,brakey = (sx+10,sy+50)
	seatbeltx,seatbelty = (sx+60,sy+50)
	batterytempx,batterytempy = (sx+110,sy+50)
	batterylowx, batterylowy = (sx+160,sy+50)
	tyrepressurex, tyrepressurey = (sx+210,sy+50)

	#cv2.rectangle(dashboard,(sx,sy),(fx,fy),(255,255,255),thickness = 5)
	#dashboard = cv2.resize(dashboard,(w,h))

	#condition to flash warning symbol here
	overlay_image(dashboard,brake,brakex,brakey,(0,0,0),(0.00,0.02,0.00))
	overlay_image(dashboard,seatbelt,seatbeltx,seatbelty,(0,0,0),(0.00,0.04,0.00))
	overlay_image(dashboard,batterytemp,batterytempx,batterytempy,(0,0,0),(0.00,0.03,0.00))
	overlay_image(dashboard,batterylow,batterylowx,batterylowy,(0,0,0),(0.00,0.04,0.00))
	overlay_image(dashboard,tyrepressure,tyrepressurex,tyrepressurey,(0,0,0),(0.0,0.006,0.0))



#start with these values
speedometer = draw_arc((x+200,y+180),100,0,360,(255,255,255),5,'0',subtextUP='SPEED',subtextDOWN='KMPH') #image of speedometer
tachometer  = draw_arc((x+310,y+80),70,0,360,(255,255,255),5,'0',subtextUP='RPM') #image of tachometer
batterymeter1 = draw_arc((x+80,y+280),70,0,360,(255,255,255),5,'0',subtextUP='BATT1',subtextDOWN='%') #image of battery1 charge
batterymeter2 = draw_arc((x+310,y+280),70,0,360,(255,255,255),5,'0',subtextUP='BATT2',subtextDOWN='%') #image of battery2 charge
current = draw_arc((x+80,y+80),70,0,360,(255,255,255),5,'37',subtextUP='I',subtextDOWN='Amps')#image of battery temperature
update_warning_symbols()

cv2.rectangle(dashboard,(0,0),(750,450),(0,255,0),thickness=5)

try:
	while 1:
		#Perform your calculations here
		number = random.randint(1,140)
		tach = random.randint(1,5000)

		#update all your values here
		update_arc(speedometer,str(number))#update car speed here
		update_arc(tachometer,str(tach))  #update rpm value here
		update_arc(batterymeter1,str(100))  #update battery1 percentage here
		update_arc(batterymeter2,str(100))  #update battery1 percentage here
		update_arc(current,'37') #update battery temperature here

		#resize an image
		#dashboard = cv2.resize(dashboard,(w,h))
		cv2.imshow('dashboard',dashboard)

		#terminating condition here
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
except KeyboardInterrupt:
	cv2.destroyAllWindows()
exit()
