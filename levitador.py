import cv2
import imutils



def write(img, texto, cor=(255,0,0), pos=(20,40)):
    fonte = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, texto, pos, fonte, 0.8, cor, 0, 
cv2.LINE_AA)

if __name__=="__main__":

    source = cv2.VideoCapture('videos/movimento.avi')


    while True:

        #Le o frame da camera/video e verifica se ouve algum erro
        r, frame = source.read()
        
        cv2.imshow('Input', frame)
        #Corta o frame para diminuir as interferencias externas
        frame = frame[70:400, 160:480]
        
        if not r: 
            print(r)
            break
        
        #Transforma o frame para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Aplica um filtro gaussiano
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        #Aplica equalização de histograma para aumentar o contraste
        #gray = cv2.equalizeHist(gray)

        #Binariza a imagem
        T , bin = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)

        #Deixa apenas os contornos na imagem
        edged = cv2.Canny(bin, 30, 200)

        #Extrai os contornos da imagem
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        #Desenha os contornos em cima do frame original
        cv2.drawContours(frame, cnts, -1, (0,255,0), 3)

        #Calcula o centro do contorno localizado        
        M = cv2.moments(cnts[0])
        cX = float(M["m10"] / M["m00"])
        cY = float(M["m01"] / M["m00"])
        #print(cX, cY)

        #Escreve na imagem os valores de X e Y do contorno
        write(frame, "Pos X: {}".format(round(cX, 1)), cor=(0,0,255))
        write(frame, "Pos Y: {}".format(round(cY, 1)), pos=(20,70),cor=(0,0,255))

        cv2.imshow('Original', frame)
        #cv2.imshow('Gray', gray)
        #cv2.imshow('Bin', edged)

        if cv2.waitKey(32) == ord('q'): 
            cv2.imwrite('back.jpg', frame)
            break