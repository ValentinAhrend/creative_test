from test_E_unreal.models import Rect, Figure


def test_to_img():

    rect2 = Rect(20, 10, 300, 100, 0, 1)
    rect3 = Rect(100, 200, 300, 400, 0, 2)
    rect4 = Rect(100, 100, 300, 120, 90, 3)
    rect1 = Rect(10, 0, 20, 10, 0, 0)
    fig = Figure([rect4, rect2, rect3, rect1])
    fig.to_img("y")
    fig.calculate_outline()


if __name__ == '__main__':
    test_to_img()

