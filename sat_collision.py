def polygon_to_polygon(points_1, points_2):
    for points in [points_1, points_2]:
        for i in range(len(points)):
            edge = (points[i], points[(i+1)%len(points)])
            edge_normal = (edge[0][1] - edge[1][1], edge[1][0] - edge[0][0])
            max_projection_1 = -1000000
            min_projection_1 = 1000000
            for point in points_1:
                projection = point[0] * edge_normal[0] + point[1] * edge_normal[1]
                if projection > max_projection_1:
                    max_projection_1 = projection
                if projection < min_projection_1:
                    min_projection_1 = projection
            max_projection_2 = -1000000
            min_projection_2 = 1000000
            for point in points_2:
                projection = point[0] * edge_normal[0] + point[1] * edge_normal[1]
                if projection > max_projection_2:
                    max_projection_2 = projection
                if projection < min_projection_2:
                    min_projection_2 = projection
            if max_projection_1 < min_projection_2 or max_projection_2 < min_projection_1:
                return False
    return True