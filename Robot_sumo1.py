import cv2 
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import numpy
import import_ipynb


#DEFININDO CÂMERA, TAMANHO, ESCALA E COORDENADAS:
webcam = cv2.VideoCapture(0)
scale = 1.3

cv2.namedWindow('CAM-1', cv2.WINDOW_NORMAL)
cv2.moveWindow('CAM-1', 430, 100)

class HandDetector:
    def __init__(self, max_hands=1, detection=0.5):

        self.max_hands = int(max_hands)
        self.detection = float(detection)

        #>>>PUXA DADOS DE UMA PASTA ESPECÍFICA PARA CONSEGUIR INTERPRETAR AS MÃOS<<<

        base_options = python.BaseOptions(model_asset_path=r'C:\Users\Aluno\Documents\Projects\Projects Python\hand_landmarker.task')
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=self.max_hands,
            min_hand_detection_confidence=self.detection
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        #PARÂMETROS PARA PASSAR PARA C++
        self.IR_FRENTE = None
        self.PARA_TRAS = None
        self.PARAR = None
        self.DIREITA = None
        self.ESQUERDA = None


    def detect_hands(self, main_cam):
        '''
        CONFIGURANDO CÂMERA E CONVERTENDO SISTEMA DE CORES 
        --> BGR PARA RGB
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
        '''OBTÉM O LADO DA MÃO(DIREITA OU ESQUERDA) PARA A FUNÇÃO
        ABAIXO NÃO DAR ERRO! ||Obs: 0 --> MÃO-1 ||
        '''
        if self.show_results.handedness:
            try:
                side = self.show_results.handedness[define_hand][0].category_name

            except IndexError:
                #>>>PARA IGNORAR ERROS<<<
                pass
            return side

    def count_fingers(self, hand_landmarks):
        '''CONTA A QUANTIDADE DE DEDOS LEVANTADO.
        LISTA DEDOS ABERTOS, DEFINE A DIREÇÃO APONTADA E RETORNA VALORES:
            1--ABERTO
            0--FECHADO
            ESQUERDA OU DIREITA
            PARAR OU AVANÇAR
        '''

        #DEDÃO É MAIS ESPECÍFICO, ELE ABRE PARA O LADO. VER NÚMERAÇÃO LAND_MARK!


        self.open_fingers = []
        
        #INFORMAÇÕES ESPECÍFICAS:

        self.BackWards = None
        Wich_Side = Detector.Right_Left_hand()
        fingertips = [8, 12, 16, 20]
        joints = [7, 11, 15, 19]

        for lm in range(4):
            
            if hand_landmarks[fingertips[lm]].y < hand_landmarks[joints[lm]].y:
                self.open_fingers.append(1)

            else:
                self.open_fingers.append(0)


        #>>>>>>>INDENTIFICAR LADO PARA IR<<<<<<<

        if Wich_Side == "Left":

            #>>>>INDENTIFICAR LADO MÃO ESQUERDA<<<<
            
            if hand_landmarks[17].x < hand_landmarks[5].x:

                self.BackWards = True


                if sum(self.open_fingers) == 0 and self.BackWards:
                    
                    if hand_landmarks[4].x > hand_landmarks[3].x:

                        #>>>VIRAR PARA ESQUERDA<<<
                        self.ESQUERDA = True
                        self.IR_FRENTE, self.PARAR, self.DIREITA == False
                        self.open_fingers.append(1)
                        print("ESQUERDA")
                
            #>>>CONTAR DEDÃO<<<
            #elif sum(self.open_fingers)
            


            else:

                self.BackWards = False

                if sum(self.open_fingers) == 0 and not self.BackWards:

                    if hand_landmarks[4].x < hand_landmarks[3].x:

                        #>>>VIRAR PARA DIREITA<<<
                        self.DIREITA = True
                        self.IR_FRENTE, self.PARAR, self.PARA_TRAS, self.DIREITA == False
                        self.open_fingers.append(1)
                        print("DIREITA")


        if Wich_Side == "Right":

            #>>>>INDENTIFICAR LADO MÃO DIREITA<<<<

            if hand_landmarks[17].x > hand_landmarks[5].x:
                self.BackWards = True

                if self.BackWards and sum(self.open_fingers) == 0:
                    
                    if hand_landmarks[4].x < hand_landmarks[3].x:

                        #>>>VIRAR PARA DIREITA<<<
                        self.DIREITA = True
                        self.IR_FRENTE, self.PARA_TRAS, self.PARAR, self.ESQUERDA == False
                        self.open_fingers.append(1)
                        print("DIREITA")

            else:

                if hand_landmarks[4].x > hand_landmarks[3].x:

                    #>>>VIRAR ESQUERDA<<<
                    self.ESQUERDA = True
                    self.IR_FRENTE, self.PARAR, self.PARA_TRAS, self.DIREITA == False
                    self.open_fingers.append(1)
                    print("ESQUERDA")

    





        
        return sum(self.open_fingers)        

    def function_hand(self,DEDOS):
        if DEDOS:

            #COLOCAR UM DELAY NO C++
            if DEDOS == "0":
                #>>>FREIO<<<
                self.IR_FRENTE, self.DIREITA, self.ESQUERDA, self.PARA_TRAS == False
                self.PARAR = True


            if DEDOS == "5":
                #>>>IR PARA FRENTE<<<
                self.IR_FRENTE = True


            elif DEDOS == "1":
                #>>>VIRAR PARA ESQUERDA<<<
                self.IR_FRENTE, self.PARAR, self.PARA_TRAS, self.DIREITA == False
                self.ESQUERDA = True


            elif DEDOS == "4":
                #>>>VIRAR PARA DIREITA<<<
                self.IR_FRENTE, self.PARA_TRAS, self.PARAR, self.ESQUERDA == False
                self.DIREITA = True


            elif DEDOS == "3":
                #>>>IR PARA TRÁS<<<
                self.IR_FRENTE, self.PARAR, self.ESQUERDA, self.DIREITA == False
                self.PARA_TRAS = True

        return DEDOS

    def Ia_Decision(self, prob=0.5):
        self.prob = prob





Detector = HandDetector()

DEDOS = "0"

while True:
    sucess, main_cam = webcam.read()

    if not sucess:
        print('\033[31mNão foi possível identificar a webcam\033[m')
        break

    x, y = main_cam.shape[:2]
    yn, xn = int(y * scale), int(x * scale)

    show_Hands = Detector.detect_hands(main_cam)

    if show_Hands:

        Detector.Draw_hand(main_cam, show_Hands)
        #PEGANDO A QUANTIDADE DE DEDOS
        Test_hand = show_Hands[0]
        num_fingers = Detector.count_fingers(Test_hand)
        DEDOS = str(num_fingers)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    

    #print(f"\033[31m{DEDOS}\033[m")

    '''if DEDOS in ["1", "2", "3", "4", "5"]:
        print(f"\033[33m{Detector.Right_Left_hand}\033[m")'''

    #ESPELHAR A WEBCAM
    imagem_certa = cv2.flip(main_cam, 1 )
    cv2.imshow("CAM-1", imagem_certa)
    cv2.resizeWindow("CAM-1", yn, xn)

#ENCERRANDO OS PROCESSOS
webcam.release()
cv2.destroyAllWindows()
