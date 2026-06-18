import cv2
import numpy as np


def transform_points(M, points):
    points_h = np.hstack((points.astype(np.float32), np.ones((points.shape[0], 1), dtype=np.float32)))
    return np.dot(M, points_h.T).T.astype(np.float32)


def build_pose_warp_points(M, target_landmarks_5, source_landmarks_5, crop_size):
    max_coord = float(crop_size - 1)
    boundary_points = np.array([
        [0.0, 0.0],
        [max_coord * 0.5, 0.0],
        [max_coord, 0.0],
        [0.0, max_coord * 0.5],
        [max_coord, max_coord * 0.5],
        [0.0, max_coord],
        [max_coord * 0.5, max_coord],
        [max_coord, max_coord],
    ], dtype=np.float32)

    inverse_M = cv2.invertAffineTransform(M)
    source_points = np.vstack((source_landmarks_5.astype(np.float32), boundary_points))
    target_points = np.vstack((target_landmarks_5.astype(np.float32), transform_points(inverse_M, boundary_points)))
    return source_points, target_points


def warp_piecewise_affine(image, source_points, target_points, output_size, interpolation, border_value):
    output_h, output_w = output_size
    output = np.zeros((output_h, output_w, *image.shape[2:]), dtype=np.float32)
    triangles = [
        (5, 6, 0), (6, 1, 0), (6, 7, 1),
        (5, 0, 8), (0, 2, 8), (8, 2, 3), (8, 3, 10),
        (0, 1, 2),
        (1, 9, 2), (9, 4, 2), (7, 9, 1), (9, 12, 4),
        (10, 3, 11), (3, 2, 11), (2, 4, 11), (11, 4, 12),
    ]

    for triangle in triangles:
        src_tri = source_points[list(triangle)].astype(np.float32)
        dst_tri = target_points[list(triangle)].astype(np.float32)

        src_rect = cv2.boundingRect(src_tri)
        dst_rect = cv2.boundingRect(dst_tri)
        src_x, src_y, src_w, src_h = src_rect
        dst_x, dst_y, dst_w, dst_h = dst_rect

        if src_w <= 0 or src_h <= 0 or dst_w <= 0 or dst_h <= 0:
            continue

        src_crop = image[src_y:src_y + src_h, src_x:src_x + src_w]
        if src_crop.size == 0:
            continue

        src_tri_rect = src_tri - np.array([src_x, src_y], dtype=np.float32)
        dst_tri_rect = dst_tri - np.array([dst_x, dst_y], dtype=np.float32)
        warp_matrix = cv2.getAffineTransform(src_tri_rect, dst_tri_rect)
        warped = cv2.warpAffine(
            src_crop,
            warp_matrix,
            (dst_w, dst_h),
            flags=interpolation,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=border_value,
        )

        mask = np.zeros((dst_h, dst_w), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.round(dst_tri_rect).astype(np.int32), 1.0, lineType=cv2.LINE_AA)

        out_x0 = max(dst_x, 0)
        out_y0 = max(dst_y, 0)
        out_x1 = min(dst_x + dst_w, output_w)
        out_y1 = min(dst_y + dst_h, output_h)
        if out_x0 >= out_x1 or out_y0 >= out_y1:
            continue

        warp_x0 = out_x0 - dst_x
        warp_y0 = out_y0 - dst_y
        warp_x1 = warp_x0 + (out_x1 - out_x0)
        warp_y1 = warp_y0 + (out_y1 - out_y0)

        warped_part = warped[warp_y0:warp_y1, warp_x0:warp_x1]
        mask_part = mask[warp_y0:warp_y1, warp_x0:warp_x1]
        if image.ndim == 3:
            mask_part = mask_part[:, :, None]

        output_roi = output[out_y0:out_y1, out_x0:out_x1]
        output[out_y0:out_y1, out_x0:out_x1] = output_roi * (1.0 - mask_part) + warped_part * mask_part

    return output


def warp_face_to_target_landmarks(image, M, target_landmarks_5, source_landmarks_5, output_size, interpolation, border_value):
    source_points, target_points = build_pose_warp_points(
        M,
        target_landmarks_5,
        source_landmarks_5,
        image.shape[0],
    )
    return warp_piecewise_affine(
        image,
        source_points,
        target_points,
        output_size,
        interpolation,
        border_value,
    )
