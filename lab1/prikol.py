def classic_map(v, min1, max1, min2, max2):
    return min2 + (v - min1) * (max2 - min2) / (max1 - min1)


    def paintScalePoints(self, pts):
        if len(self.resulting_pts) < 2:
            return
        min_x = self.width()
        min_y = self.height()
        max_x = 0
        max_y = 0
        for pt in self.resulting_pts:
            px, py = pt.x(), self.height() - pt.y()
            if px < min_x:
                min_x = px
            if py < min_y:
                min_y = py
            if px > max_x:
                max_x = px
            if py > max_y:
                max_y = py

        d_y = max_y - min_y
        d_x = max_x - min_x

        if d_y > d_x * self.height() / self.width():
            d_x = self.width() / self.height() * d_y
        else:
            d_y = self.height() / self.width() * d_x

        max_y = min_y + d_y
        max_x = min_x + d_x

        for point in pts:
            px, py = point.x(), self.height() - point.y()
            px = classic_map(px, min_x, max_x, 15, self.width() - 15)
            py = classic_map(py, min_y, max_y, 15, self.height() - 15)
            point.setX(int(px))
            point.setY(int(self.height() - py))

        self.midx = classic_map(self.midx, min_x, max_x, 15, self.width() - 15)
        self.midy = classic_map(self.midy, min_y, max_y, 15, self.height() - 15)
