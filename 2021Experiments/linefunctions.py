
F=894 //Focal length in pixels

#given camera parameters, and a point on the ground, find the x and z coordinates
#of the point, in camera centered world coordinates
#Z axis is parallel to the ground, intersecting the focal point of the camera, which is the origin.
#X axis is the horizontal axis of the image plane
#Y axis is perpendicular to the ground (i.e. real world up and down.)

def coordinatesOfPoint(h,xImg,yImg, pitch):
    thetaYC=atan(yImg/F)
    thetaXC=atan(xImg/F)
    
    thetaY=thetaYC+pitch
    z=h/thetaY
    x=z*tan(thetaXC)
    return x,z

def distanceAndAngleToLine(h,xImg1,yImg1,xImg2,yImg2,pitch):
    x1,z1=coordinatesOfPoint(h,xImg1,yImg1,pitch)
    x2,z2=coordinatesOfPoint(h,xImg2,yImg2,pitch)
    
    tanthetaL=(z2-z1)/(x2-x1)
    thetaL=atan(tanthetaL)
    #find z intercept
    z0=z1-tanthetaL*x1
    dist=z0*cos(thetaL)
    return dist,thetaL
    return
    
    
    