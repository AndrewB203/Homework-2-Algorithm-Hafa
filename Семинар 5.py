from PIL import Image, ImageDraw
import math
img =Image.open
w, h=img.size
maxr=int(math.sqrt(w*w +h*h))
accuracy=0.5
results = []
used_angles = set()
pairs={}
sorted_pairs = sorted(pairs.items(), key=lambda item: item[1], reverse=True)


for (angle, d), votes in sorted_pairs:
    if votes < threshold:  # задайте порог, например, threshold = 50
        break
    if not any(abs(angle - a) < 5 or abs(abs(angle - a) - 180) < 5 for a in used_angles):
        results.append(((angle, d), votes))
        used_angles.add(angle)


for (angle_deg, d_val), votes in results:
    print(f"Найдена прямая: угол = {angle_deg}°, расстояние = {d_val}, голосов = {votes}")


for y in range(h):
    for x in range(w):
        pixel=img.getpixel((x,y))
        if pixel==(0,0,0):
            D=math.sqrt(x*x+y*y)
            for angle in range(180):
                alpha=angle*math.pi/180
                if D==0:
                    beta=0
                else:
                    beta=math.atan2(y,x)
                d1=D*math.cos(alpha+beta-math.pi/2)
                d_rounded=round(d1)
                if abs(d1-d_rounded)<accuracy:
                    key=(angle, d_rounded)
                    pairs[key]=pairs.get(key,0)+1
if not pairs:
    print("Error")
else:
    maxkey=max(pairs.keys(), key=lambda k:pairs[k])
    maxval=pairs[maxkey]
    print(f"{maxkey} val={maxval}")
    draw =ImageDraw.Draw(img)
    angle_deg, d_val=maxkey
    angle_rad=angle_deg*math.pi/180

    points=[]

    if abs(math.sin(angle_rad))>1e-10:
        y_intersect=d_val/math.sin(angle_rad)
        if 0<=y_intersect<=h:
            points.append((0, int(y_intersect)))

    if abs(math.sin(angle_rad))>1e-10:
        y_intersect=(d_val-w*math.cos(angle_rad))/math.sin(angle_rad)
        if 0<=y_intersect<=h:
            points.append((w, int(y_intersect)))

    if abs(math.cos(angle_rad))>1e-10:
        x_intersect=d_val/math.cos(angle_rad)
        if 0<=x_intersect<=w:
            points.append((int(x_intersect), 0))

    if abs(math.cos(angle_rad))>1e-10:
        x_intersect=(d_val-math.cos(angle_rad))/math.cos(angle_rad)
        if 0<=x_intersect<=w:
            points.append((int(x_intersect), h))
    if len(points)>=2:
        draw.line([points[0],points[-1]], fill=(255, 0, 0),width=2)
        print("line is drawn")
    else:
        print("Error2")

    img.save('recling.png')
    print("picture saved")
