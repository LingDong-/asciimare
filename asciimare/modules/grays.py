# Utility for calculating the luminosity of ASCII characters of given font
# shades table for Menlo is stored, re-calculating for different fonts requires PIL library

C="`1234567890-=~!@#$%^&*()_+qwertyuiop[]\\QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:\"zxcvbnm,./ZXCVBNM<>? "

S = [(0.0, ' '), (0.072, '`'), (0.155, "'"), (0.16, '.'), (0.196, '-'), (0.214, ','), (0.226, '_'),
     (0.254, ':'), (0.283, '^'), (0.287, '!'), (0.293, '~'), (0.311, '"'), (0.332, ';'), (0.352, 'r'), 
     (0.361, '+'), (0.377, '|'), (0.379, '('), (0.382, ')'), (0.385, '/'), (0.385, '\\'), (0.392, '='), 
     (0.393, '<'), (0.393, '>'), (0.421, 'l'), (0.424, '?'), (0.444, 'i'), (0.446, 'c'), (0.453, 'v'), 
     (0.456, '['), (0.456, ']'), (0.467, 't'), (0.469, 'z'), (0.475, 'L'), (0.475, 'j'), (0.484, '7'), 
     (0.486, '*'), (0.487, 'x'), (0.488, 'f'), (0.5, '{'), (0.5, '}'), (0.509, 's'), (0.513, 'Y'), 
     (0.517, 'T'), (0.521, 'J'), (0.538, '1'), (0.54, 'C'), (0.542, 'u'), (0.547, 'n'), (0.567, 'y'), 
     (0.57, 'I'), (0.581, 'F'), (0.617, 'o'), (0.621, 'w'), (0.625, 'e'), (0.626, 'V'), (0.626, 'k'), 
     (0.627, '2'), (0.636, 'h'), (0.637, '3'), (0.64, 'Z'), (0.644, 'a'), (0.652, '4'), (0.659, 'X'), 
     (0.676, '%'), (0.677, 'S'), (0.678, '5'), (0.695, 'P'), (0.705, '$'), (0.712, 'm'), (0.717, 'E'), 
     (0.718, 'G'), (0.726, 'A'), (0.733, 'U'), (0.752, 'b'), (0.752, 'd'), (0.752, 'q'), (0.753, 'p'), 
     (0.766, 'K'), (0.773, '9'), (0.774, '6'), (0.775, 'O'), (0.784, '#'), (0.786, 'H'), (0.793, '&'), 
     (0.797, 'D'), (0.821, 'R'), (0.834, 'Q'), (0.835, 'g'), (0.836, '8'), (0.877, '0'), (0.887, 'W'), 
     (0.901, 'M'), (0.909, 'B'), (0.92, '@'), (1.0, 'N')]

# calculate shades table for a font by drawing it and reading the pixels
def glyphshades(PIL,fontfile):
    S = {}
    w,h = 70,120
    smin = w*h
    smax = 0

    for i in range(0,len(C)):
        im = PIL.Image.new("RGB",(w,h))
        dr = PIL.ImageDraw.Draw(im)
        font = PIL.ImageFont.truetype(fontfile, 100)
        dr.text((0, 0),C[i],(255,255,255),font=font)
        S[C[i]]=0
        px = im.load()

        for y in range(0,im.size[1]):
            for x in range(0,im.size[0]):
                r, g, b = px[x,y][:3]
                if r > 128 and g > 128 and b > 128:
                    S[C[i]]+=1

        if S[C[i]]<smin: smin=S[C[i]]
        if S[C[i]]>smax: smax=S[C[i]]

    def mapval(value,istart,istop,ostart,ostop):
        return ostart + (ostop - ostart) * ((value - istart)*1.0 / (istop - istart))
    def dec3(x):
        return int(x * 1000)/1000.0

    S = sorted([(dec3(mapval(S[k],smin,smax,0,1)),k) for k in S.keys()])
    return S

# re-calculate for a given font, requires PIL
def recalculate(fontfile):
    global S
    import PIL
    from PIL import Image, ImageFont, ImageDraw
    S = glyphshades(PIL,fontfile)

# returns a character of the closest shade given a value (0-1)
def getshade(x):
    if x < 0: return S[0][1]
    if x > 1: return S[-1][1]
    for i in range(1,len(S)):
        if S[i-1][0] <= x <= S[i][0]:
            if abs(x-S[i-1][0]) < abs(x-S[i][0]):
                return S[i-1][1]
            else:
                return S[i][1]
    return ""

if __name__ == "__main__":
    # recalculate("fonts/Menlo.ttc")
    out = ""
    n = 301
    for i in range(0,n):
        x = i*1.0/n
        out += getshade(x)
        if i % 60 == 0:
            out += "\n"
    print out
