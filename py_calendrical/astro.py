from __future__ import division
from mpmath import mpf
from py_cal_cal import ifloor
from py_calendrical.triganometry import angle, tan_degrees, arctan_degrees
from py_calendrical.day_arithmatic import DayOfWeek
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.location import Location, URBANA
from py_calendrical.time_arithmatic import Clock

def urbana_sunset(gdate):
    """Return sunset time in Urbana, Ill, on Gregorian date 'gdate'."""
    return Clock.time_from_moment(URBANA.sunset(gdate.to_fixed()))

def urbana_winter(g_year):
    """Return standard time of the winter solstice in Urbana, Illinois, USA."""
    return URBANA.standard_from_universal(Location.solar_longitude_after(Location.WINTER, GregorianDate(g_year, JulianMonth.January, 1).to_fixed()))

def jewish_dusk(date, location):
    """Return standard time of Jewish dusk on fixed date, date,
    at location, location, (as per Vilna Gaon)."""
    return location.dusk(date, angle(4, 40, 0))

def jewish_sabbath_ends(date, location):
    """Return standard time of end of Jewish sabbath on fixed date, date,
    at location, location, (as per Berthold Cohn)."""
    return location.dusk(date, angle(7, 5, 0)) 

def jewish_morning_end(date, location):
    """Return standard time on fixed date, date, at location, location,
    of end of morning according to Jewish ritual."""
    return location.standard_from_sundial(date + Clock.days_from_hours(10))

def asr(date, location):
    """Return standard time of asr on fixed date, date,
    at location, location."""
    noon = location.universal_from_standard(location.midday(date))
    phi = location.latitude
    delta = Location.declination(noon, 0, Location.solar_longitude(noon))
    altitude = delta - phi - 90
    h = arctan_degrees(tan_degrees(altitude), 2 * tan_degrees(altitude) + 1)
    # For Shafii use instead:
    # tan_degrees(altitude) + 1)
    return location.dusk(date, -h)

JERUSALEM = Location(mpf(31.8), mpf(35.2), 800, Clock.days_from_hours(2))

def astronomical_easter(g_year):
    """Return date of (proposed) astronomical Easter in Gregorian
    year, g_year."""
    jan1 = GregorianDate.new_year(g_year)
    equinox = Location.solar_longitude_after(Location.SPRING, jan1)
    paschal_moon = ifloor(JERUSALEM.apparent_from_local(JERUSALEM.local_from_universal(Location.lunar_phase_at_or_after(Location.FULL, equinox))))
    # Return the Sunday following the Paschal moon.
    return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)
