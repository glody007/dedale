def x(point):
    return point[0]

def y(point):
    return point[1]

def width(rectangle):
    return rectangle[0]

def height(rectangle):
    return rectangle[1]

def fromPointToCm(x):
    return (x * 2.54) / 72

def rightSideOutOfBound(page_size, child):
    child_origin_x    = x(child.getAbsoluteOrigin())
    page_width        = width(page_size)
    child_width       = width(child.getSize())
    child_extremity_x = child_origin_x + child_width
    is_out_of_bound   = page_width < child_extremity_x
    return is_out_of_bound

def leftSideOutOfBound(page_size, child):
    child_origin_x    = x(child.getAbsoluteOrigin())
    is_out_of_bound   = child_origin_x < 0
    return is_out_of_bound

def lowerSideOutOfBound(page_size, child):
    child_origin_y    = y(child.getAbsoluteOrigin())
    page_height       = height(page_size)
    child_height      = height(child.getSize())
    child_extremity_y = child_origin_y + child_height
    is_out_of_bound   = page_height < child_extremity_y
    return is_out_of_bound

def upperSideOutOfBound(page_size, child):
    child_origin_y    = y(child.getAbsoluteOrigin())
    is_out_of_bound   = child_origin_y < 0
    return is_out_of_bound

def sizeFromPointToCm(size):
    x = fromPointToCm(size[0])
    y = fromPointToCm(size[1])
    return (x, y)

def isInRange(minimum, maximum, position):
    is_in_range = (position <= maximum
                   and position >= minimum)
    return is_in_range

def isInSideRange(container_side_size,
                  element_side_size,
                  side_origin):
    side_extremity  = (side_origin +
                       element_side_size)
    is_origin_in_range = isInRange(0,
                            container_side_size,
                            side_origin)
    is_extrem_in_range = isInRange(0,
                             container_side_size,
                             side_extremity)
    is_in_range = (is_origin_in_range and
                   is_extrem_in_range)
    return is_in_range

def isInWidthRange(container_size,
                   element_size,
                   origin):
    return isInSideRange(width(container_size),
                         width(element_size),
                         x(origin))

def isInHeightRange(container_size,
                    element_size,
                    origin):
    return isInSideRange(height(container_size),
                         height(element_size),
                         y(origin))

def inPageBound(page_size, child):
    in_width_range = isInWidthRange(page_size,
                                    child.getSize(),
                                    child.getAbsoluteOrigin())
    in_height_range = isInHeightRange(page_size,
                                      child.getSize(),
                                      child.getAbsoluteOrigin())
    in_bound =  in_width_range and in_height_range
    return in_bound

def autoHorizontalMargin(container_size, element_size):
    delta_x = x(container_size) - x(element_size)
    side_margin = delta_x / 2
    return {"left": side_margin,
            "right": side_margin,
            "top": 0,
            "bottom": 0}

def autoVerticalMargin(container_size, element_size):
    delta_y = y(container_size) - y(element_size)
    side_margin = delta_y / 2
    return {"left": 0,
            "right": 0,
            "top": side_margin,
            "bottom": side_margin}
