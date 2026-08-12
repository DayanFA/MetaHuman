import cv2
import mediapipe as mp
from pythonosc import udp_client

# Configurar o transmissor OSC local na porta 8050
client = udp_client.SimpleUDPClient("127.0.0.1", 8050)

# 1. Inicializar o módulo Pose (para Tronco e Braços)
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# 2. Inicializar o módulo Hands (para as Mãos e Dedos detalhados)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2, 
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

escala = 100.0  # Conversão para centímetros da Unreal
print("Rastreamento Simultâneo (Tronco, Braços e Mãos) para LIBRAS iniciado...")

cv2.namedWindow("LIBRAS - Corpo e Maos", cv2.WINDOW_AUTOSIZE)

while True:
    success, img = cap.read()
    if not success:
        break

    # Espelhar a imagem para movimento natural
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Processar ambos os modelos no mesmo frame
    results_pose = pose.process(img_rgb)
    results_hands = hands.process(img_rgb)

    # --- 1. PROCESSAR E ENVIAR DADOS DO CORPO/BRAÇOS ---
    if results_pose.pose_world_landmarks:
        landmarks = results_pose.pose_world_landmarks.landmark
        
        # 11: Ombro Direito | 13: Cotovelo Direito | 16: Pulso Direito
        ombro_dir = landmarks[11]
        cotovelo_dir = landmarks[13]
        pulso_dir = landmarks[16]
        
        od_x, od_y, od_z = -ombro_dir.z * escala, ombro_dir.x * escala, -ombro_dir.y * escala
        cd_x, cd_y, cd_z = -cotovelo_dir.z * escala, cotovelo_dir.x * escala, -cotovelo_dir.y * escala
        pd_x, pd_y, pd_z = -pulso_dir.z * escala, pulso_dir.x * escala, -pulso_dir.y * escala

        client.send_message("/corpo/ombro_dir", [od_x, od_y, od_z])
        client.send_message("/corpo/cotovelo_dir", [cd_x, cd_y, cd_z])
        client.send_message("/corpo/pulso_dir", [pd_x, pd_y, pd_z])

        mp_draw.draw_landmarks(img, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # --- 2. PROCESSAR E ENVIAR DADOS DETALHADOS DAS MÃOS ---
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Coleta os 21 pontos detalhados de cada mão
            dados_mao = []
            for landmark in hand_landmarks.landmark:
                dados_mao.extend([landmark.x, landmark.y, landmark.z])
            
            client.send_message("/libras/mao_completa", dados_mao)

    cv2.imshow("LIBRAS - Corpo e Maos", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()