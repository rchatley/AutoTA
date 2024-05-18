package ic.doc;

import com.weather.Day;

public enum WeatherDay {

  MONDAY(Day.MONDAY),
  TUESDAY(Day.TUESDAY),
  WEDNESDAY(Day.WEDNESDAY),
  THURSDAY(Day.THURSDAY),
  FRIDAY(Day.FRIDAY),
  SATURDAY(Day.SATURDAY),
  SUNDAY(Day.SUNDAY);

  private final com.weather.Day day;

  WeatherDay(com.weather.Day day) {
    this.day = day;
  }

  public Day getDay() {
    return day;
  }
}