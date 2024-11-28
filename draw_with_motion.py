import cv2  # Biblioteca para processamento de imagens e captura de vídeo.
from cvzone.HandTrackingModule import HandDetector  # Módulo de detecção de mãos da biblioteca cvzone.

video = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # Inicializa a câmera (índice 0) com otimização para Windows (CAP_DSHOW).

video.set(3,1280)  # Define a largura da imagem capturada em pixels.
video.set(4,720)   # Define a altura da imagem capturada em pixels.


detector = HandDetector()  # Cria o objeto detector de mãos.
desenho = []  # Lista que armazenará as coordenadas dos pontos do desenho.


while True:
    check,img = video.read()  # Captura um frame da câmera.
    resultado = detector.findHands(img,draw=True)  # Detecta mãos no frame e desenha as marcações (opcional).
    hand = resultado[0]  # Extrai a primeira mão detectada (se houver).

# Se uma mão for detectada:
    if hand:
        lmlist = hand[0]['lmList']  # Lista de coordenadas dos pontos-chave da mão.
        dedos = detector.fingersUp(hand[0])  # Verifica quais dedos estão levantados.
        dedosLev = dedos.count(1)  # Conta o número de dedos levantados.

#Desenho com o Indicador (1 dedo levantado):
        if dedosLev==1:  
            x,y = lmlist[8][0],lmlist[8][1]  # Coordenadas da ponta do dedo indicador (ponto 8).
            cv2.circle(img,(x,y),15,(0,0,255),cv2.FILLED)  # Desenha um círculo na ponta do indicador.
            desenho.append((x,y))  # Adiciona o ponto à lista do desenho.

#"Levantar o lápis" (nenhum dedo ou mais de 1, exceto 3):
        elif dedosLev !=1 and dedosLev !=3:  
            desenho.append((0,0))  # Marca uma quebra na linha do desenho.
#Limpar o desenho (3 dedos levantados):
        elif dedosLev==3:  
            desenho = []  # Reseta a lista do desenho.

#Desenho na Tela
        for id,ponto in enumerate(desenho):  # Itera pelos pontos da lista de desenho.
            x,y = ponto[0],ponto[1]  # Obtém as coordenadas do ponto atual.
            cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)  # Desenha um círculo no ponto.

            if id >=1:  # A partir do segundo ponto:
                ax,ay = desenho[id-1][0],desenho[id-1][1]  # Obtém as coordenadas do ponto anterior.
                if x!=0 and ax!=0:  # Verifica se ambos os pontos são válidos (não são quebras).
                    cv2.line(img,(x,y),(ax,ay),(0,0,255),20)  # Conecta os pontos com uma linha.

#Exibição e Controle do Programa
    imgFlip = cv2.flip(img,1)  # Espelha a imagem horizontalmente para facilitar a interação.
    cv2.imshow('Img',imgFlip)  # Exibe o frame processado em uma janela.
    if cv2.waitKey(1) & 0xFF == 27:  # Sai do loop se a tecla 'Esc' for pressionada.
        break

#Liberação de Recursos
video.release()  # Libera a câmera.
cv2.destroyAllWindows()  # Fecha todas as janelas abertas pelo OpenCV.
