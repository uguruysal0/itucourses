import cv2
import numpy as np
import os
from scipy import signal
import flow_vis


def get_data(directory):
    global R
    global C
    elems = []
    for root, dirs, files in os.walk(directory):
        files.sort()
        for file in files:
            if file.endswith(".jpg"):
                img = cv2.imread(os.path.join(root, file))
                img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                elems.append(img_gray)

    return np.array(elems).transpose(1, 2, 0)


def optical_flow(I_1, I_2, window_size=3, threshold=1e-2):
    w, h = I_1.shape
    window_size = window_size // 2
    u, v = np.zeros((w, h)), np.zeros((w, h))
    kernel_x = np.array([[-1., 1.],
                         [-1., 1.]])

    kernel_t = np.array([[1., 1.],
                         [1., 1.]])

    # gradients respect x,y and t
    fx = signal.convolve2d(I_1, kernel_x, mode="same")
    fy = signal.convolve2d(I_1, kernel_x.T, mode="same")
    ft = signal.convolve2d(I_2, kernel_t, mode="same") - \
        signal.convolve2d(I_1, kernel_t, mode="same")

    for i in range(window_size, w-window_size):
        for j in range(window_size, h-window_size):

            Ix = fx[i-window_size:i+window_size+1, j -
                    window_size:j+window_size+1].flatten()
            Iy = fy[i-window_size:i+window_size+1, j -
                    window_size:j+window_size+1].flatten()
            It = ft[i-window_size:i+window_size +
                    1, j-window_size:j+window_size+1].flatten()

            # construct the linear equation system Ax = b
            # x = (A.T*A)-1A.T*b
            b = np.reshape(It, (It.shape[0], 1))
            A = np.vstack((Ix, Iy)).T

            if np.min(abs(np.linalg.eigvals(np.matmul(A.T, A)))) >= threshold:
                # refactor the
                nu = np.matmul(np.linalg.pinv(A), b)  # get velocity here
                u[i, j] = nu[0]
                v[i, j] = nu[1]

    return (u, v)


def lucas_kanade(video):
    flow_video = []
    video = video / 255.
    for i in range(video.shape[2] - 1):
        u, v = optical_flow(video[..., i], video[..., i+1], 3)
        flow_uv = np.array([u, v]).transpose(1, 2, 0)
        flow_color = flow_vis.flow_to_color(flow_uv, convert_to_bgr=True)
        flow_video.append(flow_color)
        if i > 5:
            break

    return flow_video


def video_creator(images):
    frame_width, frame_height = images[0].shape[0], images[0].shape[1]
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
    for i in images:
        out.write(i)
    out.release()


def save_video(directory, images):
    try:
        os.mkdir(directory)
    except:
        pass

    prefix = directory+"/"
    suffix = ".jpg"
    for i in range(len(images)):
        cv2.imwrite(prefix+str(i)+suffix, images[i])


# video = get_data("traffic_sequence")
# images = lucas_kanade(video)
# save_video("optic_flows", images)
