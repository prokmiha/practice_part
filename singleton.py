class CornerCounter:
    _instance = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(CornerCounter, cls).__new__(cls)
        return cls._instance

    def corner_counter(self, time: str):
        hours, minutes = time.split('.')
        minutes = int(minutes)
        one_minute_corner = 360 / 60
        hours = int(hours) * 5
        if hours == 60:
            hours = 0
        if minutes == 0:
            minutes = 60

        result = (minutes - hours) * one_minute_corner
        return result if result > 0 else -result


singleton = CornerCounter()

result = singleton.corner_counter(input("Введите время в формате (час в 12 часовом формате) . (минуты)\n"))
print(result)