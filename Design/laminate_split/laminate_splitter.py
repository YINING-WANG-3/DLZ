import cv2
import numpy as np
import time
import math

# function to find closest value
def closest(lst, K):
    clo = lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
    return clo

# function to find closest and min value
def smal_closest(lst, K):
    lst.append(K)
    lst = sorted(lst)
    i = lst.index(K)
    if i >= 1:
        clo = lst[i-1]
    else:
        clo = K
    return clo

def big_closest(lst, K):
    lst.append(K)
    lst = sorted(lst)
    i = lst.index(K)
    if i < len(lst)-1:
        clo = lst[i+1]
    else:
        clo = K
    return clo

# function to devide by two
def divide2(n):
    n1 = n // 2
    n2 = n - n1
    return n1, n2

# function to devide by five
def divide5(x, n):
    x = x*10
    m = x // n
    m1 = 5 * round(m/5)
    m2 = x - (n-1)*m1
    return m1/10 ,m2/10

# function to split
def splitter(l_all, w_all, standard):
    start = time.time()
    
    l_all = l_all / 10
    w_all = w_all / 10
    
    w = w_all
    
    zone = [[0,282], [282,552], [552,822], [822,10920]]
    print(zone)
    
    # list all l_b
    zone_d = []
    for n in range(2,5):
        d = int(60 * (n - 0.5))
        while d <= 60*n:
            zone_d.append(d)
            d += 5
    print(zone_d)
    
    # national rules
    if standard == '国标':
        l_f = 30
        # determine l_b, l_d
        num_d = 0
        for i in zone:
            if zone.index(i) == 0 and l_all <= i[1] and l_all > i[0]:
                tri = 0
                num_d = zone.index(i) + 1
                l_d = l_all
                l_b = 0
            elif zone.index(i) > 0 and l_all <= i[1] and l_all > i[0]:
                tri = 0
                num_d = zone.index(i) + 1
                l_b = round((l_all - l_f * zone.index(i)) / num_d, 1)
                l_b = closest(zone_d, l_b)
                l_d = l_all - (l_b + l_f) * zone.index(i)
                # adjust for special circumstances
                if l_d <= 240 and zone.index(i) == 2:
                    tri = 2
                elif l_d > 240 and zone.index(i) == 2:
                    tri = 1
                    l_b = max(zone_d)
                    l_d = (l_all - l_f * zone.index(i) - l_b * (zone.index(i) - 1))/2
                elif l_d > 261 and zone.index(i) == 1:
                    tri = 0
                    l_b = round((l_all - l_f * zone.index(i)) / 2, 2)
                    l_d = l_all - (l_b + l_f) * zone.index(i)
                elif l_d > 261 and zone.index(i) > 2:
                    tri = 1
                    l_b = max(zone_d)
                    l_d = (l_all - l_f * zone.index(i) - l_b * (zone.index(i) - 1))/2
        
        # determine num
        num = 2*num_d - 1
        
        # draw image
        img = np.ones((800, 1200, 3), dtype = np.uint8)
        img = 255* img

        for m in range(num):
            if tri == 0:
                # draw b
                if m % 2 == 0 and m != num - 1 and l_b in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+l_b+m/2*(l_b+l_f)), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                elif m % 2 == 0 and m != num - 1 and l_b not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+l_b+m/2*(l_b+l_f)), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_b*10, 1)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                # draw f
                elif m%2 == 1 and m != num - 1:
                    cv2.rectangle(img, (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b), int(400-w/2)), (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b+l_f), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f*10)), (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b-10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                # draw d
                elif m == num - 1 and l_d not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+m/2*(l_b+l_f)+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                elif m == num - 1 and l_d in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+m/2*(l_b+l_f)+l_d), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_d*10)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
            elif tri == 1:
                # draw first d
                if m == 0:
                    cv2.rectangle(img, (int(600-l_all/2), int(400-w/2)), (int(600-l_all/2+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2 + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                # draw f
                elif m%2 == 1 and m != num - 1:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m//2*(l_f+l_b)), int(400-w/2)), (int(600-l_all/2+l_d+m//2*(l_f+l_b)+l_f), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f*10)), (int(600-l_all/2+l_d+m//2*(l_f+l_b) - 10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                # draw b
                elif m % 2 == 0 and m != num - 1 and m != 0:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b), int(400-w/2)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b+l_b), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw last d
                elif m == num - 1:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b), int(400-w/2)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
            elif tri == 2:
                # draw first b
                if m == 0:
                    cv2.rectangle(img, (int(600-l_all/2), int(400-w/2)), (int(600-l_all/2+l_b), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw f
                elif m%2 == 1:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m//2*(l_f+l_d)), int(400-w/2)), (int(600-l_all/2+l_b+m//2*(l_f+l_d)+l_f), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f*10)), (int(600-l_all/2+l_b+m//2*(l_f+l_d) - 10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                # draw d
                elif m % 2 == 0 and m != num - 1 and l_d not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d), int(400-w/2)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                elif m % 2 == 0 and m != num - 1 and l_d in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d), int(400-w/2)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+l_d), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_d*10)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw last b
                elif m == num - 1:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d), int(400-w/2)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+l_b), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                    
    # Guangdong rules           
    elif standard == '广东省标':
        l_f = 30
        # determine l_b, l_d
        num_d = 0
        for i in zone:
            if zone.index(i) == 0 and l_all <= i[1] and l_all > i[0]:
                tri = 0
                num_d = zone.index(i) + 1
                l_d = l_all
                l_b = 0
            elif zone.index(i) > 0 and l_all <= i[1] and l_all > i[0]:
                tri = 0
                num_d = zone.index(i) + 1
                l_b = round((l_all - l_f * zone.index(i)) / num_d, 1)
                l_b = closest(zone_d, l_b)
                l_d = l_all - (l_b + l_f) * zone.index(i)
                # adjust for special circumstances
                if l_d <= 240 and zone.index(i) == 2:
                    tri = 2
                elif l_d > 240 and zone.index(i) == 2:
                    tri = 1
                    l_b = max(zone_d)
                    l_d = (l_all - l_f * zone.index(i) - l_b * (zone.index(i) - 1))/2
                elif l_d > 261 and zone.index(i) == 1:
                    tri = 0
                    l_b = round((l_all - l_f * zone.index(i)) / 2, 2)
                    l_d = l_all - (l_b + l_f) * zone.index(i)
                elif l_d > 261 and zone.index(i) > 2:
                    tri = 1
                    l_b = max(zone_d)
                    l_d = (l_all - l_f * zone.index(i) - l_b * (zone.index(i) - 1))/2
                print("The split mode is:" + str(tri))
                # adjust l_f
                l_d_c = smal_closest(zone_d, l_d)
                zone_d.remove(l_d)
                l_d_2 = l_d
                l_f_2 = l_f
                if tri == 1 and l_d_2 not in zone_d:
                    if 2*(l_d - l_d_c) <= 10 * zone.index(i) and l_d not in zone_d and l_d - l_d_c != 0:
                        diff = 2*(l_d - l_d_c)
                        l_d = l_d_2 = l_d_c
                        l_f_old = l_f
                        l_f = l_f_old + divide5(diff, zone.index(i))[0]
                        l_f_2 = l_f_old + divide5(diff, zone.index(i))[1]
                    elif l_d - l_d_c <= 10 * zone.index(i) <= 2*(l_d - l_d_c) and l_d not in zone_d and l_d - l_d_c != 0:
                        diff = l_d - l_d_c
                        l_d_2 = l_d_c
                        l_f_old = l_f
                        l_f = l_f_old + divide5(diff, zone.index(i))[0]
                        l_f_2 = l_f_old + divide5(diff, zone.index(i))[1]
                elif (tri == 0 or tri == 2) and l_d not in zone_d:
                    if l_d - l_d_c <= 10 * zone.index(i) and l_d not in zone_d and l_d - l_d_c != 0:
                        diff = l_d - l_d_c
                        l_d = l_d_c
                        l_f_old = l_f
                        l_f = l_f_old + divide5(diff, zone.index(i))[0]
                        l_f_2 = l_f_old + divide5(diff, zone.index(i))[1]
                # adjust l_b
                if (tri == 0 or tri == 2) and l_d not in zone_d:
                    if l_b == 180 or l_b == 120 or l_b == 215:
                        l_d_c_2 = big_closest(zone_d, l_d)
                        zone_d.remove(l_d)
                        diff_b = math.ceil((l_d_c_2 - l_d) / (zone.index(i) * 5))
                        l_b = l_b - diff_b * 5
                        l_d_tem = l_d + diff_b * zone.index(i) * 5
                        if l_d_tem not in zone_d:
                            l_d = smal_closest(zone_d, l_d_tem)
                            zone_d.remove(l_d_tem)
                            diff_2 = l_d_tem - l_d
                            l_f_old = l_f
                            l_f = l_f_old + divide5(diff_2, zone.index(i))[0]
                            l_f_2 = l_f_old + divide5(diff_2, zone.index(i))[1]
                        else:
                            l_d = l_d_tem
                    elif l_b == 150 or l_b == 210:
                        l_d_c_2 = smal_closest(zone_d, l_d)
                        zone_d.remove(l_d)
                        diff_b = math.ceil((l_d - l_d_c_2) / (zone.index(i) * 5))
                        l_b = l_b + diff_b * 5
                        l_d_tem = l_d - diff_b * zone.index(i) * 5
                        if l_d_tem not in zone_d:
                            l_d = smal_closest(zone_d, l_d_tem)
                            zone_d.remove(l_d_tem)
                            diff_2 = l_d_tem - l_d
                            l_f_old = l_f
                            l_f = l_f_old + divide5(diff_2, zone.index(i))[0]
                            l_f_2 = l_f_old + divide5(diff_2, zone.index(i))[1]
                        else:
                            l_d = l_d_tem
                # reduce type by l_f and l_d
                if tri == 1 and l_d_2 != l_b:
                    com = zone.index(i)*40-l_f*(zone.index(i)-1)-l_f_2
                    if l_d_2 < l_b:
                        if (zone.index(i)-1) * (l_b - l_d_2) <= com and l_b in zone_d and l_d_2 in zone_d:
                            diff_3 = (zone.index(i)-1) * (l_b - l_d_2)
                            l_b = l_d_2
                            l_f_old = l_f
                            l_f = l_f_old + divide5(diff_3, zone.index(i))[0]
                            l_f_2 = l_f_old + divide5(diff_3, zone.index(i))[1]
                        elif 2*(l_d_2 - (l_d_2+l_b)/2) + (zone.index(i)-1)*(l_b - (l_d_2+l_b)/2) <= com and l_b in zone_d and l_d_2 in zone_d:
                            diff_3 = 2*(l_d_2 - (l_d_2+l_b)/2) + (zone.index(i)-1)*(l_b - (l_d_2+l_b)/2)
                            if (l_d_2+l_b)/2 in zone_d:
                                l_b = l_d_2 = (l_d_2+l_b)/2
                                l_f_old = l_f
                                l_f = l_f_old + divide5(diff_3, zone.index(i))[0]
                                l_f_2 = l_f_old + divide5(diff_3, zone.index(i))[1]
                                ppt.append(l_all)
                        elif (l_d_2 + (zone.index(i)-1) * l_b) / zone.index(i) in zone_d:
                            l_d_2 = l_b = (l_d_2 + (zone.index(i)-1) * l_b) / zone.index(i)
                elif (tri == 0 or tri == 2) and l_d != l_b:
                    com = zone.index(i)*40-l_f*(zone.index(i)-1)-l_f_2
                    if l_d > l_b:
                        if l_d - l_b <= com and l_d in zone_d and l_b in zone_d:
                            diff_3 = l_d - l_b
                            l_d = l_b
                            l_f_old = l_f
                            l_f = l_f_old + divide5(diff_3, zone.index(i))[0]
                            l_f_2 = l_f_old + divide5(diff_3, zone.index(i))[1]
                        elif (zone.index(i)-1)*(l_d-(l_d+l_b)/2) <= com and l_d in zone_d and l_b in zone_d:
                            diff_3 = (zone.index(i)-1)*(l_d-(l_d+l_b)/2)
                            if (l_d+l_b)/2 in zone_d:
                                l_d = l_b = (l_d+l_b)/2
                                l_f_old = l_f
                                l_f = l_f_old + divide5(diff_3, zone.index(i))[0]
                                l_f_2 = l_f_old + divide5(diff_3, zone.index(i))[1]
                        elif (l_d + zone.index(i) * l_b) / (zone.index(i) + 1) in zone_d:
                            l_d = l_b = (l_d + zone.index(i) * l_b) / (zone.index(i) + 1)
                    elif l_d < l_b:
                        if zone.index(i) * (l_b - l_d) <= com and l_d in zone_d and l_b in zone_d:
                            diff_3 = zone.index(i) * (l_b - l_d)
                            l_b = l_d
                            l_f_old = l_f
                            l_f = l_f_old + divide5(diff_3, zone.index(i))[0]
                            l_f_2 = l_f_old + divide5(diff_3, zone.index(i))[1]
                        elif (zone.index(i)-1)*(l_b-(l_d+l_b)/2) <= com and l_d in zone_d and l_b in zone_d:
                            diff_3 = (zone.index(i)-1)*(l_b-(l_d+l_b)/2)
                            if (l_d+l_b)/2 in zone_d:
                                l_b = l_d = (l_d+l_b)/2
                                l_f_old = l_f
                                l_f = l_f_old + divide5(diff_3, zone.index(i))[0]
                                l_f_2 = l_f_old + divide5(diff_3, zone.index(i))[1]
                        elif (l_d + zone.index(i) * l_b) / (zone.index(i) + 1) in zone_d:
                            l_d = l_b = (l_d + zone.index(i) * l_b) / (zone.index(i) + 1)
        
        # determine num
        num = 2*num_d - 1
        
        # draw image
        img = np.ones((800, 1200, 3), dtype = np.uint8)
        img = 255* img
        for m in range(num):
            if tri == 0:
                # draw b
                if m % 2 == 0 and m != num - 1 and l_b in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+l_b+m/2*(l_b+l_f)), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                elif m % 2 == 0 and m != num - 1 and l_b not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+l_b+m/2*(l_b+l_f)), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_b*10, 1)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                # draw f
                elif m%2 == 1 and m != num - 2:
                    cv2.rectangle(img, (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b), int(400-w/2)), (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b+l_f), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f*10)), (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b-10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                elif m == num - 2:
                    cv2.rectangle(img, (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b), int(400-w/2)), (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b+l_f_2), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f_2*10)), (int(600-l_all/2+m//2*l_f+(m//2+1)*l_b-10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                # draw d
                elif m == num - 1 and l_d not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+m/2*(l_b+l_f)+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                elif m == num - 1 and l_d in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+m/2*(l_b+l_f)), int(400-w/2)), (int(600-l_all/2+m/2*(l_b+l_f)+l_d), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_d*10)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
            elif tri == 1:
                # draw first d
                if m == 0 and l_d not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2), int(400-w/2)), (int(600-l_all/2+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2 + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                elif m == 0 and l_d in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2), int(400-w/2)), (int(600-l_all/2+l_d), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2 + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw f
                elif m%2 == 1 and m != num - 2:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m//2*(l_f+l_b)), int(400-w/2)), (int(600-l_all/2+l_d+m//2*(l_f+l_b)+l_f), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f*10)), (int(600-l_all/2+l_d+m//2*(l_f+l_b) - 10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                elif m == num - 2:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m//2*(l_f+l_b)), int(400-w/2)), (int(600-l_all/2+l_d+m//2*(l_f+l_b)+l_f_2), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f_2*10)), (int(600-l_all/2+l_d+m//2*(l_f+l_b) - 10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                # draw b
                elif m % 2 == 0 and m != num - 1 and m != 0:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b), int(400-w/2)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b+l_b), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw last d
                elif m == num - 1 and l_d_2 not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b), int(400-w/2)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b+l_d_2), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d_2*10, 1)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                elif m == num - 1 and l_d_2 in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b), int(400-w/2)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b+l_d_2), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(round(l_d_2*10, 1)), (int(600-l_all/2+l_d+m/2*l_f+(m/2-1)*l_b + 20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
            elif tri == 2:
                # draw first b
                if m == 0:
                    cv2.rectangle(img, (int(600-l_all/2), int(400-w/2)), (int(600-l_all/2+l_b), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw f
                elif m%2 == 1 and m != num - 2:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m//2*(l_f+l_d)), int(400-w/2)), (int(600-l_all/2+l_b+m//2*(l_f+l_d)+l_f), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f*10)), (int(600-l_all/2+l_b+m//2*(l_f+l_d) - 10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                elif m == num - 2:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m//2*(l_f+l_d)), int(400-w/2)), (int(600-l_all/2+l_b+m//2*(l_f+l_d)+l_f_2), int(400+w/2)), (225,225,225), 2)
                    cv2.putText(img, str(int(l_f_2*10)), (int(600-l_all/2+l_b+m//2*(l_f+l_d) - 10), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (225,225,225), 2)
                # draw d
                elif m % 2 == 0 and m != num - 1 and l_d not in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d), int(400-w/2)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+l_d), int(400+w/2)), (150,150,150), 2)
                    cv2.putText(img, str(round(l_d*10, 1)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150,150,150), 2)
                elif m % 2 == 0 and m != num - 1 and l_d in zone_d:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d), int(400-w/2)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+l_d), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_d*10)), (int(600-l_all/2+m/2*(l_b+l_f)+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
                # draw last b
                elif m == num - 1:
                    cv2.rectangle(img, (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d), int(400-w/2)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+l_b), int(400+w/2)), (255,0,0), 2)
                    cv2.putText(img, str(int(l_b*10)), (int(600-l_all/2+l_b+m/2*l_f+(m/2-1)*l_d+20), int(400-w/2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    
    # draw l_all, w_all
    cv2.putText(img, str(int(l_all*10)), (600-30, int(400+w/2 + 30)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    cv2.putText(img, str(int(w_all*10)), (int(600-l_all/2 - 80), 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    
    # execution time
    end = time.time()
    print("The time of execution of above program is:", round(end-start, 4), "s")
    
    # show image
    '''cv2.imshow('Splitter', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    
    # save image
    filename = str(l_all*10) + '.png'
    cv2.imwrite(filename, img)

# split laminate
'''a = int(input("Please enter length: "))
b = int(input("Please enter width: "))'''
'''splitter(3350, 3200, '广东省标')'''

# batch split laminate
ppt = []
for i in range(2830, 10930, 10):
    splitter(i, 3200, '广东省标')
print(ppt)