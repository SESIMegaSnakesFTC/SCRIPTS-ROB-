import cv2 
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import time



#DEFININDO CÂMERA, TAMANHO, ESCALA E COORDENADAS:


webcam = cv2.VideoCapture(0)
scale = 1.3
cv2.namedWindow('CAM-1', cv2.WINDOW_NORMAL)
cv2.moveWindow('CAM-1', 430, 100)



class HandDetector:
    

    
    def __init__(self, max_hands=1, detection=0.5):


        self.inicio = None
        self.max_hands = int(max_hands)
        self.detection = float(detection)


        #>>>PUXA A API PARA CONSEGUIR INTERPRETAR AS MÃOS<<<


        base_options = python.BaseOptions(model_asset_path=r'C:\Users\Aluno\Documents\Projects\Projects Python\ROBOTICA\hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=self.max_hands,
            min_hand_detection_confidence=self.detection
        )        
        self.detector = vision.HandLandmarker.create_from_options(options)


        #PARÂMETROS PARA PASSAR PARA C++

        self.State = None



    def detect_hands(self, main_cam):

        '''
        CONFIGURANDO CÂMERA E CONVERTENDO SISTEMA DE CORES 
        ---> BGR PARA RGB
        '''

        imgRGB = cv2.cvtColor(main_cam, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
        self.show_results = self.detector.detect(mp_image)
        return self.show_results.hand_landmarks
    
        
        
    def Draw_hand(self, main_cam, hand_landmarks_list):
        
        '''Converte landmarks da nova API para o formato do draw_landmarks'''
        
        mp_draw = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands


        for hand_landmarks in hand_landmarks_list:

            landmark_list = landmark_pb2.NormalizedLandmarkList()
            landmark_list.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=lm.x, y=lm.y, z=lm.z)
                for lm in hand_landmarks
            ])
            mp_draw.draw_landmarks(main_cam, landmark_list, mp_hands.HAND_CONNECTIONS)
    
    
    def Right_Left_hand(self, define_hand=0):
        
        '''DEFINE O LADO DA MÃO  --->  DIREITA OU ESQUERDA
        '''
        try:
            if self.show_results.handedness:

                '''A API do mediapipe retorna a mão direita como "Right" e a mão esquerda como "Left".
                ---> *Dependendo da versão da lib, precisa usar outra função*
                '''
                self.side = self.show_results.handedness[define_hand][0].category_name

        
        except IndexError:
            self.side = None
            
        return self.side
            

    def thumb_open(self, hand_landmarks):
        

        '''VERIFICA SE O DEDÃO ESTÁ ABERTO OU FECHADO, INDEPENDENTE DA ORIENTAÇÃO.
            ---> RETORNA TRUE OU FALSE.
        '''    


        #>>>INFORMAÇÕES ESPECÍFICAS PARA A FUNÇÃO DE CONTAGEM DE DEDOS<<<
        
        self.hand_landmarks = hand_landmarks
        self.thumb_is_open = None
        self.inversed = None
        
        
        
        #>>>>FUNÇÃO MAIN<<<<
        if self.side == "Left":
            
            
            #>>>INVERTIDO<<<
            if hand_landmarks[17].x < hand_landmarks[5].x:
                
                #>>>DEDÃO INVERTIDO<<<
                self.inversed = True
                
            
                if hand_landmarks[4].x > hand_landmarks[3].x:
                    
                    #>>>DEDÃO ABERTO<<<
                    self.thumb_is_open = True
                    
                    
                    
                else:
                    
                    #>>>DEDÃO FECHADO<<<
                    self.thumb_is_open = False
            
            
            else:
                
            #>>>MÃO NORMAL<<<

                self.inversed = False
                
                
                if hand_landmarks[4].x < hand_landmarks[3].x:
                    
                    #>>>DEDÃO ABERTO<<<
                    self.thumb_is_open = True
                    
                    
                else:
                    
                    #>>>DEDÃO FECHADO<<<
                    self.thumb_is_open = False
                    
                    
                    
        else:
            
        #>>>MÃO DIREITA<<<
        
            #>>>INVERTIDO<<<

            if hand_landmarks[17].x > hand_landmarks[5].x:
                
                #>>>DEDÃO INVERTIDO<<<
                self.inversed = True
                
                
                
                if hand_landmarks[4].x < hand_landmarks[3].x:
                    
                    #>>>DEDÃO ABERTO<<<
                    self.thumb_is_open = True
                    
                    
                    
                else:
                    
                    #>>>DEDÃO FECHADO<<<
                    self.thumb_is_open = False
                    
                    
            else:

                self.inversed = False
                
                if hand_landmarks[4].x > hand_landmarks[3].x:
                    
                    #>>>DEDÃO ABERTO<<<
                    self.thumb_is_open = True
                    
                    
                else:
                    
                    #>>>DEDÃO FECHADO<<<
                    self.thumb_is_open = False
                    
    

    def Timer(self, condition = None, duration_time = 3):


        '''FUNÇÃO PARA DETERMINAR O TEMPO TRUE OU FALSE SE UMA FUNÇÃO ESTIVER SENDO EXECUTADA
        POR UM TEMPO DETERMINADO.
        '''



        if condition:


            if self.inicio is None:

                #>>>INICIO DA CONTAGEM<<<
                self.inicio = time.monotonic()


            if time.monotonic() - self.inicio >= duration_time:

                #>>>TEMPO EXCEDIDO<<<
                return True
            

        else:

            #>>>NÃO ESTÁ SENDO EXECUTADO<<<

            self.inicio = None

        return False
        

    
    def count_fingers(self, hand_landmarks):


        '''CONTA A QUANTIDADE DE DEDOS LEVANTADO.
        LISTA DEDOS ABERTOS, DEFINE A DIREÇÃO APONTADA E RETORNA VALORES:
        
        1--ABERTO
        0--FECHADO
        ESQUERDA OU DIREITA
        PARAR OU AVANÇAR
        '''


        #>>>LISTA DE DEDOS ABERTOS<<<
        self.open_fingers = []
        
        
        
        #==}}INFORMAÇÕES ESPECÍFICAS{{==

        self.BackWards = None
        fingertips = [8, 12, 16, 20]
        joints = [7, 11, 15, 19]


        #>>>CONTANDO OS DEDOS MÉDIOS<<<
        
        for lm in range(4):
            
            
            if hand_landmarks[fingertips[lm]].y < hand_landmarks[joints[lm]].y:
                
                self.open_fingers.append(1)



            else:

                self.open_fingers.append(0)



        #>>>DEFININDO DIREÇÕES/SINAIS<<<
        
                
        if self.thumb_is_open: 
            
            
            #>>CONTAR DEDO ABERTO<<<
            
            self.open_fingers.append(1)
        
        
            #>>>DIREÇÕES<<<


            
            if sum(self.open_fingers) == 1:
                
                
                if self.side == "Left" and self.inversed == False:
                    
                    
                    self.State = "DIREITA"



                elif self.side == "Left" and self.inversed == True:
                    
                    
                    self.State = "ESQUERDA"



                elif self.side == "Right" and self.inversed == False:

                    
                    self.State = "ESQUERDA"
                    
                    
                    
                elif self.side == "Right" and self.inversed == True:
                    
                    
                    
                    self.State = "DIREITA"
                    
                    
                    
            elif sum(self.open_fingers) == 5:
                    
                    
                    self.State = "AVANÇAR"
                    
                    
                                
        elif sum(self.open_fingers) == 0:

            #>>>SE O DEDÃO ESTIVER FECHADO<<<
            
            self.open_fingers.append(0) 
            self.State = "PARAR"
            

            self.Backward = Detector.Timer(condition = True, duration_time = 3)


            if self.Backward:

                self.State = "RECUAR"

            else:

                self.State = "PARAR"
            

        if sum(self.open_fingers) != 0:
            
            self.BackWards = False
            self.inicio = None
            


        return self.State




#>>>INSTÂNCIA DA CLASSE<<<
Detector = HandDetector()


while True:
    
    
    sucess, main_cam = webcam.read()

    if not sucess:
        print('\033[31mNão foi possível identificar a webcam\033[m')
        break

    #>>>OPCIONAL --> AUMENTANDO A JANELA SIZE<<<
    
    x, y = main_cam.shape[:2]
    yn, xn = int(y * scale), int(x * scale)
    

    #===>>>VARIÁVEL PARA ARMAZENAR AS INFORMAÇÕES DAS MÃOS<<<===
    
    show_Hands = Detector.detect_hands(main_cam)


    #===>EXECUÇÃO DAS FUNÇÕES<===
    
    if show_Hands:

        Detector.Draw_hand(main_cam, show_Hands)
        My_hand = show_Hands[0]
    
        Detector.Right_Left_hand()
        Detector.thumb_open(My_hand)
        Detector.count_fingers(My_hand)
        
        print(f"\033[32m{Detector.State}\033[m")
        
        
    #===>>>TECLA DE FUGA<<<===
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    

        
    
    #>>>ESPELHAR A WEBCAM<<<
    
    imagem_certa = cv2.flip(main_cam, 1 )
    cv2.imshow("CAM-1", imagem_certa)
    cv2.resizeWindow("CAM-1", yn, xn)
    

#ENCERRANDO OS PROCESSOS
webcam.release()
cv2.destroyAllWindows()