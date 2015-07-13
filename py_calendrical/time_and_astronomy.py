from mpmath import atan2, degrees, sin, cos, tan, mpf, atan, asin, acos
from operator import mod

######################
# Time and Astronomy #
######################
def ecliptical_from_equatorial(ra, declination, obliquity):
    """Convert equatorial coordinates (in degrees) to ecliptical ones.
    'declination' is the declination,
    'ra' is the right ascension and
    'obliquity' is the obliquity of the ecliptic.
    NOTE: if 'apparent' right ascension and declination are used, then 'true'
          obliquity should be input.
    """
    co = cos_degrees(obliquity)
    so = sin_degrees(obliquity)
    sa = sin_degrees(ra)
    lon = normalized_degrees_from_radians(
        atan2(sa*co + tan_degrees(declination)*so, cos_degrees(ra)))
    lat = arcsin_degrees(
            sin_degrees(declination)*co -
            cos_degrees(declination)*so*sa)
    return [lon, lat]

def equatorial_from_ecliptical(longitude, latitude, obliquity):
    """Convert ecliptical coordinates (in degrees) to equatorial ones.
    'longitude' is the ecliptical longitude,
    'latitude'  is the ecliptical latitude and
    'obliquity' is the obliquity of the ecliptic.
    NOTE: resuting 'ra' and 'declination' will be referred to the same equinox
          as the one of input ecliptical longitude and latitude.
    """
    co = cos_degrees(obliquity)
    so = sin_degrees(obliquity)
    sl = sin_degrees(longitude)
    ra = normalized_degrees_from_radians(
        atan2(sl*co - tan_degrees(latitude)*so,
        cos_degrees(longitude)))
    dec = arcsin_degrees(
            sin_degrees(latitude)*co +
            cos_degrees(latitude)*so*sl)
    return [ra, dec]

def horizontal_from_equatorial(H, declination, latitude):
    """Convert equatorial coordinates (in degrees) to horizontal ones.
    Return 'azimuth' and 'altitude'.
    'H'            is the local hour angle,
    'declination'  is the declination,
    'latitude'     is the observer's geographic latitude.
    NOTE: 'azimuth' is measured westward from the South.
    NOTE: This is not a good formula for using near the poles.
    """
    ch = cos_degrees(H)
    sl = sin_degrees(latitude)
    cl = cos_degrees(latitude)
    A = normalized_degrees_from_radians(
            atan2(sin_degrees(H), 
                  ch * sl - tan_degrees(declination) * cl))
    h = arcsin_degrees(sl * sin_degrees(declination) + 
                       cl * cos_degrees(declination) * ch)
    return [A, h]

def equatorial_from_horizontal(A, h, phi):
    """Convert equatorial coordinates (in degrees) to horizontal ones.
    Return 'local hour angle' and 'declination'.
    'A'   is the azimuth,
    'h'   is the altitude,
    'phi' is the observer's geographical latitude.
    NOTE: 'azimuth' is measured westward from the South.
    """
    H = normalized_degrees_from_radians(
            atan2(sin_degrees(A), 
                  (cos_degrees(A) * sin_degrees(phi) + 
                   tan_degrees(h) * cos_degrees(phi))))
    delta = arcsin_degrees(sin_degrees(phi) * sin_degrees(h) - 
                           cos_degrees(phi) * cos_degrees(h) * cos_degrees(A))
    return [H, delta]

# see lines 2667-2670 in calendrica-3.0.cl
def days_from_hours(x):
    """Return the number of days given x hours."""
    return x / 24

# see lines 2672-2675 in calendrica-3.0.cl
def days_from_seconds(x):
    """Return the number of days given x seconds."""
    return x / 24 / 60 / 60

# see lines 2677-2680 in calendrica-3.0.cl
def mt(x):
    """Return x as meters."""
    return x

# see lines 2682-2686 in calendrica-3.0.cl
def deg(x):
    """Return the degrees in angle x."""
    return x

# see lines 2688-2690 in calendrica-3.0.cl
def secs(x):
    """Return the seconds in angle x."""
    return x / 3600

# see lines 2692-2696 in calendrica-3.0.cl
def angle(d, m, s):
    """Return an angle data structure
    from d degrees, m arcminutes and s arcseconds.
    This assumes that negative angles specifies negative d, m and s."""
    return d + ((m + (s / 60)) / 60)

# see lines 2698-2701 in calendrica-3.0.cl
def normalized_degrees(theta):
    """Return a normalize angle theta to range [0,360) degrees."""
    return mod(theta, 360)

# see lines 2703-2706 in calendrica-3.0.cl
def normalized_degrees_from_radians(theta):
    """Return normalized degrees from radians, theta.
    Function 'degrees' comes from mpmath."""
    return normalized_degrees(degrees(theta))

# see lines 2708-2711 in calendrica-3.0.cl
def radians_from_degrees(theta):
    pass
from mpmath import radians as radians_from_degrees

# see lines 2713-2716 in calendrica-3.0.cl
def sin_degrees(theta):
    """Return sine of theta (given in degrees)."""
    #from math import sin
    return sin(radians_from_degrees(theta))

# see lines 2718-2721 in calendrica-3.0.cl
def cos_degrees(theta):
    """Return cosine of theta (given in degrees)."""
    #from math import cos
    return cos(radians_from_degrees(theta))

# from errata20091230.pdf entry 112
cos_degrees=cos_degrees


# see lines 2723-2726 in calendrica-3.0.cl
def tan_degrees(theta):
    """Return tangent of theta (given in degrees)."""
    return tan(radians_from_degrees(theta))

# from errata20091230.pdf entry 112
tan_degrees=tan_degrees


def signum(a):
    if a > 0:
        return 1
    elif a == 0:
        return 0
    else:
        return -1

#-----------------------------------------------------------
# NOTE: arc[tan|sin|cos] casted with degrees given CL code
#       returns angles [0, 360), see email from Dershowitz
#       after my request for clarification
#-----------------------------------------------------------

# see lines 2728-2739 in calendrica-3.0.cl
# def arctan_degrees(y, x):
#     """ Arctangent of y/x in degrees."""
#     from math import atan2
#     return normalized_degrees_from_radians(atan2(x, y))

def arctan_degrees(y, x):
   """ Arctangent of y/x in degrees."""
   if (x == 0) and (y != 0):
       return mod(signum(y) * deg(mpf(90)), 360)
   else:
       alpha = normalized_degrees_from_radians(atan(y / x))
       if x >= 0:
           return alpha
       else:
           return mod(alpha + deg(mpf(180)), 360)


# see lines 2741-2744 in calendrica-3.0.cl
def arcsin_degrees(x):
    """Return arcsine of x in degrees."""
    #from math import asin
    return normalized_degrees_from_radians(asin(x))

# see lines 2746-2749 in calendrica-3.0.cl
def arccos_degrees(x):
    """Return arccosine of x in degrees."""
    #from math import acos
    return normalized_degrees_from_radians(acos(x))

class Location(object):
    
    def __init(self, latitude, longitude, elevation, zone):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.zone = zone
        
# see lines 2771-2775 in calendrica-3.0.cl
MECCA = Location(angle(21, 25, 24), angle(39, 49, 24), mt(298), days_from_hours(3))

# see lines 5898-5901 in calendrica-3.0.cl
JERUSALEM = Location(31.8, 35.2, mt(800), days_from_hours(2))

BRUXELLES = Location(angle(4, 21, 17), angle(50, 50, 47), mt(800), days_from_hours(1))

URBANA = Location(40.1, -88.2, mt(225), days_from_hours(-6))

GREENWHICH = Location(51.4777815, 0, mt(46.9), days_from_hours(0))

# see lines 2777-2797 in calendrica-3.0.cl
def direction(location, focus):
    """Return the angle (clockwise from North) to face focus when
    standing in location, location.  Subject to errors near focus and
    its antipode."""
    phi = location.latitude
    phi_prime = focus.latitude
    psi = location.longitude
    psi_prime = focus.longitude
    y = sin_degrees(psi_prime - psi)
    x = ((cos_degrees(phi) * tan_degrees(phi_prime)) -
         (sin_degrees(phi)    * cos_degrees(psi - psi_prime)))
    if ((x == y == 0) or (phi_prime == deg(90))):
        return deg(0)
    elif (phi_prime == deg(-90)):
        return deg(180)
    else:
        return arctan_degrees(y, x)

# see lines 2799-2803 in calendrica-3.0.cl
def standard_from_universal(tee_rom_u, location):
    """Return standard time from tee_rom_u in universal time at location."""
    return tee_rom_u + location.zone

# see lines 2805-2809 in calendrica-3.0.cl
def universal_from_standard(tee_rom_s, location):
    """Return universal time from tee_rom_s in standard time at location."""
    return tee_rom_s - location.zone

# see lines 2811-2815 in calendrica-3.0.cl
def zone_from_longitude(phi):
    """Return the difference between UT and local mean time at longitude
    'phi' as a fraction of a day."""
    return phi / deg(360)

# see lines 2817-2820 in calendrica-3.0.cl
def local_from_universal(tee_rom_u, location):
    """Return local time from universal tee_rom_u at location, location."""
    return tee_rom_u + zone_from_longitude(location.longitude)

# see lines 2822-2825 in calendrica-3.0.cl
def universal_from_local(tee_ell, location):
    """Return universal time from local tee_ell at location, location."""
    return tee_ell - zone_from_longitude(location.longitude)

# see lines 2827-2832 in calendrica-3.0.cl
def standard_from_local(tee_ell, location):
    """Return standard time from local tee_ell at locale, location."""
    return standard_from_universal(universal_from_local(tee_ell, location),
                                   location)

# see lines 2834-2839 in calendrica-3.0.cl
def local_from_standard(tee_rom_s, location):
    """Return local time from standard tee_rom_s at location, location."""
    return local_from_universal(universal_from_standard(tee_rom_s, location),
                                location)

# see lines 2841-2844 in calendrica-3.0.cl
def apparent_from_local(tee, location):
    """Return sundial time at local time tee at location, location."""
    return tee + equation_of_time(universal_from_local(tee, location))

# see lines 2846-2849 in calendrica-3.0.cl
def local_from_apparent(tee, location):
    """Return local time from sundial time tee at location, location."""
    return tee - equation_of_time(universal_from_local(tee, location))

# see lines 2851-2857 in calendrica-3.0.cl
def midnight(date, location):
    """Return standard time on fixed date, date, of true (apparent)
    midnight at location, location."""
    return standard_from_local(local_from_apparent(date, location), location)

# see lines 2859-2864 in calendrica-3.0.cl
def midday(date, location):
    """Return standard time on fixed date, date, of midday
    at location, location."""
    return standard_from_local(local_from_apparent(date + days_from_hours(mpf(12)),
                                                   location), location)

# see lines 2866-2870 in calendrica-3.0.cl
def julian_centuries(tee):
    """Return Julian centuries since 2000 at moment tee."""
    return (dynamical_from_universal(tee) - J2000) / mpf(36525)

# see lines 2872-2880 in calendrica-3.0.cl
def obliquity(tee):
    """Return (mean) obliquity of ecliptic at moment tee."""
    c = julian_centuries(tee)
    return (angle(23, 26, mpf(21.448)) +
            poly(c, [mpf(0),
                     angle(0, 0, mpf(-46.8150)),
                     angle(0, 0, mpf(-0.00059)),
                     angle(0, 0, mpf(0.001813))]))

def precise_obliquity(tee):
    """Return precise (mean) obliquity of ecliptic at moment tee."""
    u = julian_centuries(tee)/100
    #assert(abs(u) < 1,
    #       'Error! This formula is valid for +/-10000 years around J2000.0')
    return (poly(u, [angle(23, 26, mpf(21.448)),
                     angle(0, 0, mpf(-4680.93)),
                     angle(0, 0, mpf(-   1.55)),
                     angle(0, 0, mpf(+1999.25)),
                     angle(0, 0, mpf(-  51.38)),
                     angle(0, 0, mpf(- 249.67)),
                     angle(0, 0, mpf(-  39.05)),
                     angle(0, 0, mpf(+   7.12)),
                     angle(0, 0, mpf(+  27.87)),
                     angle(0, 0, mpf(+   5.79)),
                     angle(0, 0, mpf(+   2.45))]))

def true_obliquity(tee):
    """Return 'true' obliquity of ecliptic at moment tee.
    That is, where nutation is taken into accout."""
    pass


# see lines 2882-2891 in calendrica-3.0.cl
def declination(tee, beta, lam):
    """Return declination at moment UT tee of object at
    longitude 'lam' and latitude 'beta'."""
    varepsilon = obliquity(tee)
    return arcsin_degrees(
        (sin_degrees(beta) * cos_degrees(varepsilon)) +
        (cos_degrees(beta) * sin_degrees(varepsilon) * sin_degrees(lam)))

# see lines 2893-2903 in calendrica-3.0.cl
def right_ascension(tee, beta, lam):
    """Return right ascension at moment UT 'tee' of object at
    latitude 'lam' and longitude 'beta'."""
    varepsilon = obliquity(tee)
    return arctan_degrees(
        (sin_degrees(lam) * cos_degrees(varepsilon)) -
        (tan_degrees(beta) * sin_degrees(varepsilon)),
        cos_degrees(lam))

# see lines 2905-2920 in calendrica-3.0.cl
def sine_offset(tee, location, alpha):
    """Return sine of angle between position of sun at 
    local time tee and when its depression is alpha at location, location.
    Out of range when it does not occur."""
    phi = location.latitude
    tee_prime = universal_from_local(tee, location)
    delta = declination(tee_prime, deg(mpf(0)), solar_longitude(tee_prime))
    return ((tan_degrees(phi) * tan_degrees(delta)) +
            (sin_degrees(alpha) / (cos_degrees(delta) *
                                   cos_degrees(phi))))

# see lines 2922-2947 in calendrica-3.0.cl
def approx_moment_of_depression(tee, location, alpha, early):
    """Return the moment in local time near tee when depression angle
    of sun is alpha (negative if above horizon) at location;
    early is true when MORNING event is sought and false for EVENING.
    Returns BOGUS if depression angle is not reached."""
    ttry  = sine_offset(tee, location, alpha)
    date = fixed_from_moment(tee)

    if (alpha >= 0):
        if early:
            alt = date
        else:
            alt = date + 1
    else:
        alt = date + days_from_hours(12)

    if (abs(ttry) > 1):
        value = sine_offset(alt, location, alpha)
    else:
        value = ttry


    if (abs(value) <= 1):
        temp = -1 if early else 1
        temp *= mod(days_from_hours(12) + arcsin_degrees(value) / deg(360), 1) - days_from_hours(6)
        temp += date + days_from_hours(12)
        return local_from_apparent(temp, location)
    else:
        return BOGUS

# see lines 2949-2963 in calendrica-3.0.cl
def moment_of_depression(approx, location, alpha, early):
    """Return the moment in local time near approx when depression
    angle of sun is alpha (negative if above horizon) at location;
    early is true when MORNING event is sought, and false for EVENING.
    Returns BOGUS if depression angle is not reached."""
    tee = approx_moment_of_depression(approx, location, alpha, early)
    if (tee == BOGUS):
        return BOGUS
    else:
        if (abs(approx - tee) < days_from_seconds(30)):
            return tee
        else:
            return moment_of_depression(tee, location, alpha, early)

# see lines 2965-2968 in calendrica-3.0.cl
MORNING = True

# see lines 2970-2973 in calendrica-3.0.cl
EVENING = False

# see lines 2975-2984 in calendrica-3.0.cl
def dawn(date, location, alpha):
    """Return standard time in morning on fixed date date at
    location location when depression angle of sun is alpha.
    Returns BOGUS if there is no dawn on date date."""
    result = moment_of_depression(date + days_from_hours(6), location, alpha, MORNING)
    if (result == BOGUS):
        return BOGUS
    else:
        return standard_from_local(result, location)

# see lines 2986-2995 in calendrica-3.0.cl
def dusk(date, location, alpha):
    """Return standard time in evening on fixed date 'date' at
    location 'location' when depression angle of sun is alpha.
    Return BOGUS if there is no dusk on date 'date'."""
    result = moment_of_depression(date + days_from_hours(18), location, alpha, EVENING)
    if (result == BOGUS):
        return BOGUS
    else:
        return standard_from_local(result, location)

# see lines 440-451 in calendrica-3.0.errata.cl
def refraction(tee, location):
    """Return refraction angle at location 'location' and time 'tee'."""
    from math import sqrt
    h     = max(mt(0), location.elevation)
    cap_R = mt(6.372E6)
    dip   = arccos_degrees(cap_R / (cap_R + h))
    return angle(0, 50, 0) + dip + secs(19) * sqrt(h)

# see lines 2997-3007 in calendrica-3.0.cl
def sunrise(date, location):
    """Return Standard time of sunrise on fixed date 'date' at
    location 'location'."""
    alpha = refraction(date, location)
    return dawn(date, location, alpha)

# see lines 3009-3019 in calendrica-3.0.cl
def sunset(date, location):
    """Return standard time of sunset on fixed date 'date' at
    location 'location'."""
    alpha = refraction(date, location)
    return dusk(date, location, alpha)

# see lines 453-458 in calendrica-3.0.errata.cl
def observed_lunar_altitude(tee, location):
    """Return the observed altitude of moon at moment, tee, and
    at location, location,  taking refraction into account."""
    return topocentric_lunar_altitude(tee, location) + refraction(tee, location)

# see lines 460-467 in calendrica-3.0.errata.cl
def moonrise(date, location):
    """Return the standard time of moonrise on fixed, date,
    and location, location."""
    t = universal_from_standard(date, location)
    waning = (lunar_phase(t) > deg(180))
    alt = observed_lunar_altitude(t, location)
    offset = alt / 360
    if (waning and (offset > 0)):
        approx =  t + 1 - offset
    elif waning:
        approx = t - offset
    else:
        approx = t + (1 / 2) + offset
    rise = binary_search(approx - days_from_hours(3),
                         approx + days_from_hours(3),
                         lambda u, l: ((u - l) < days_from_hours(1 / 60)),
                         lambda x: observed_lunar_altitude(x, location) > deg(0))
    return standard_from_universal(rise, location) if (rise < (t + 1)) else BOGUS


def urbana_sunset(gdate):
    """Return sunset time in Urbana, Ill, on Gregorian date 'gdate'."""
    return time_from_moment(sunset(fixed_from_gregorian(gdate), URBANA))

# from eq 13.38 pag. 191
def urbana_winter(g_year):
    """Return standard time of the winter solstice in Urbana, Illinois, USA."""
    return standard_from_universal(
               solar_longitude_after(
                   WINTER, 
                   fixed_from_gregorian(gregorian_date(g_year, JANUARY, 1))),
               URBANA)
