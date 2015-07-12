# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

##############################################################################
# The idea is to use the Appendix C in "Calendrical Calculations", 3rd Ed    #
# values to check the correctness (or the same erroneusness !-) of the       #
# Python implementation.                                                     #
##############################################################################

# read each row and transform the first cell in the various calendar and the
# check the result
import csv
class AppendixCTable1TestCaseBase():
    """This class provides methods to load the relevant test data and helpers."""

    def _dayOfWeek(self, d):
        return self._wdDict[d]

    def _romanLeap(self, c):
        return False if c == 'f' else True

    def setUp(self):
        self._wdDict = {'Sunday': SUNDAY,
                        'Monday': MONDAY,
                        'Tuesday': TUESDAY,
                        'Wednesday': WEDNESDAY,
                        'Thursday': THURSDAY,
                        'Friday': FRIDAY,
                        'Saturday': SATURDAY}

        reader = csv.reader(open("dates1.csv", "rU"),
                            delimiter=',',
                            quoting=csv.QUOTE_NONE)
        self.rd    = [] # Rata Die
        self.wd    = [] # WeekDay
        self.jd    = [] # Julian Day
        self.mjd   = [] # Madified Julian Day
        self.gd    = [] # Gregorian Date
        self.isod  = [] # ISO Date
        self.jdt   = [] # Julian DaTe
        self.jrn   = [] # Julian Roman Name
        self.ed    = [] # Egyptian Date
        self.ad    = [] # Armenian Date
        self.cd    = [] # Coptic Date

        for row in reader:
            self.rd.append(int(row[0]))
            self.wd.append(self._dayOfWeek(row[1]))
            self.jd.append(float(row[2]))
            self.mjd.append(int(row[3]))
            self.gd.append(
                gregorian_date(int(row[4]), int(row[5]), int(row[6])))
            self.isod.append(
                iso_date(int(row[7]), int(row[8]), int(row[9])))
            self.jdt.append(
                julian_date(int(row[10]), int(row[11]), int(row[12])))
            self.jrn.append(roman_date(int(row[13]),
                                       int(row[14]),
                                       int(row[15]),
                                       int(row[16]),
                                       self._romanLeap(row[17])))
            self.ed.append(
                egyptian_date(int(row[18]), int(row[19]), int(row[20])))
            self.ad.append(
                armenian_date(int(row[21]), int(row[22]), int(row[23])))
            self.cd.append(
                coptic_date(int(row[24]), int(row[25]), int(row[26])))


class AppendixCTable1TestCase(AppendixCTable1TestCaseBase, unittest.TestCase):
    def testWeekdays(self):
        for i in range(len(self.rd)):
            # weekdays
            self.assertEqual(day_of_week_from_fixed(self.rd[i]), self.wd[i])

    def testJulian(self):
        for i in range(len(self.rd)):
            # julian date
            self.assertEqual(julian_from_fixed(self.rd[i]), self.jdt[i])
            self.assertEqual(fixed_from_julian(self.jdt[i]), self.rd[i])
            # julian date, roman name
            self.assertEqual(roman_from_fixed(self.rd[i]), self.jrn[i])
            self.assertEqual(fixed_from_roman(self.jrn[i]), self.rd[i])

    def testGregorian(self):
        for i in range(len(self.rd)):
            self.assertEqual(gregorian_from_fixed(self.rd[i]), self.gd[i])
            self.assertEqual(fixed_from_gregorian(self.gd[i]), self.rd[i])
            self.assertEqual(
                gregorian_year_from_fixed(self.rd[i]), standard_year(self.gd[i]))

    def testAltGregorian(self):
        for i in range(len(self.rd)):
            self.assertEqual(alt_gregorian_from_fixed(self.rd[i]), self.gd[i])
            self.assertEqual(alt_fixed_from_gregorian(self.gd[i]), self.rd[i])
            self.assertEqual(
                alt_gregorian_year_from_fixed(self.rd[i]),
                standard_year(self.gd[i]))

    def testIso(self):
        for i in range(len(self.rd)):
            self.assertEqual(iso_from_fixed(self.rd[i]), self.isod[i])
            self.assertEqual(fixed_from_iso(self.isod[i]), self.rd[i])

    def testEgyptian(self):
        for i in range(len(self.rd)):
            self.assertEqual(egyptian_from_fixed(self.rd[i]), self.ed[i])
            self.assertEqual(fixed_from_egyptian(self.ed[i]), self.rd[i])


    def testArmenian(self):
        for i in range(len(self.rd)):
            self.assertEqual(armenian_from_fixed(self.rd[i]), self.ad[i])
            self.assertEqual(fixed_from_armenian(self.ad[i]), self.rd[i])


    def testCoptic(self):
        for i in range(len(self.rd)):
            self.assertEqual(coptic_from_fixed(self.rd[i]), self.cd[i])
            self.assertEqual(fixed_from_coptic(self.cd[i]), self.rd[i])



class AppendixCTable2TestCaseBase():
    def setUp(self):
        reader = csv.reader(open("dates2.csv", "rU"),
                            delimiter=',',
                            quoting=csv.QUOTE_NONE)
        self.rd    = [] # Rata Die
        self.ed    = [] # Ethiopic Date
        self.id    = [] # Islamic Date
        self.io    = [] # Islamic Observational date
        self.bd    = [] # Bahai Date
        self.bf    = [] # Bahai Future date
        self.mlc   = [] # Mayan Long Count
        self.mh    = [] # Mayan Haab
        self.mt    = [] # Mayan Tzolkin
        self.ax    = [] # Aztec Xihuitl
        self.at    = [] # Aztec Tonalpohualli

        for row in reader:
            self.rd.append(int(row[0]))
            self.ed.append(
                ethiopic_date(int(row[1]), int(row[2]), int(row[3])))
            self.id.append(
                islamic_date(int(row[4]), int(row[5]), int(row[6])))
            self.io.append(
                islamic_date(int(row[7]), int(row[8]), int(row[9])))
            self.bd.append(
                bahai_date(int(row[10]), int(row[11]), int(row[12]),
                           int(row[13]), int(row[14])))
            self.bf.append(
                bahai_date(int(row[15]), int(row[16]), int(row[17]),
                           int(row[18]), int(row[19])))
            self.mlc.append(
                mayan_long_count_date(int(row[20]), int(row[21]),
                                      int(row[22]), int(row[23]),
                                                  int(row[24])))
            self.mh.append(
                mayan_haab_date(int(row[25]), int(row[26])))
            self.mt.append(
                mayan_tzolkin_date(int(row[27]), int(row[28])))
            self.ax.append(
                aztec_xihuitl_date(int(row[29]), int(row[30])))
            self.at.append(
                aztec_tonalpohualli_date(int(row[31]), int(row[32])))

 
class AppendixCTable2TestCase(AppendixCTable2TestCaseBase,
                               unittest.TestCase):
    def testEthiopic(self):
        for i in range(len(self.rd)):
            # ethiopic day
            self.assertEqual(ethiopic_from_fixed(self.rd[i]), self.ed[i])
            self.assertEqual(fixed_from_ethiopic(self.ed[i]), self.rd[i])


    def testIslamic(self):
        for i in range(len(self.rd)):
            # islamic
            self.assertEqual(islamic_from_fixed(self.rd[i]), self.id[i])
            self.assertEqual(fixed_from_islamic(self.id[i]), self.rd[i])
            # islamic (observational)
            self.assertEqual(
                fixed_from_observational_islamic(self.io[i]), self.rd[i])
            self.assertEqual(
                observational_islamic_from_fixed(self.rd[i]), self.io[i])


    def testBahai(self):
        for i in range(len(self.rd)):
            # bahai
            self.assertEqual(bahai_from_fixed(self.rd[i]), self.bd[i])
            self.assertEqual(fixed_from_bahai(self.bd[i]), self.rd[i])
            # bahai future
            self.assertEqual(future_bahai_from_fixed(self.rd[i]), self.bf[i])
            self.assertEqual(fixed_from_future_bahai(self.bf[i]), self.rd[i])


    def testMayan(self):
        for i in range(len(self.rd)):
            # mayan (long count)
            self.assertEqual(
                mayan_long_count_from_fixed(self.rd[i]), self.mlc[i])
            self.assertEqual(
                fixed_from_mayan_long_count(self.mlc[i]), self.rd[i])
            # mayan (haab)
            self.assertEqual(mayan_haab_from_fixed(self.rd[i]), self.mh[i])
            # mayan (tzolkin)
            self.assertEqual(mayan_tzolkin_from_fixed(self.rd[i]), self.mt[i])

    def testAztec(self):
        for i in range(len(self.rd)):
            # aztec xihuitl
            self.assertEqual(aztec_xihuitl_from_fixed(self.rd[i]), self.ax[i])
            # aztec tonalpohualli
            self.assertEqual(
                aztec_tonalpohualli_from_fixed(self.rd[i]), self.at[i])


 
class AppendixCTable3TestCaseBase():

    def _toBoolean(self, c):
        return False if c == 'f' else True

    def setUp(self):
        reader = csv.reader(open("dates3.csv", "rU"),
                            delimiter=',',
                            quoting=csv.QUOTE_NONE)
        self.rd    = []
        self.hd    = [] # hebrew standard
        self.ho    = [] # hebrew observational
        self.je    = [] # julian easter
        self.ge    = [] # gregorian easter
        self.ae    = [] # astronomical easter
        self.bd    = [] # balinese pawukon
        self.pas   = [] # persian astronomical
        self.par   = [] # persian arithmetic
        self.fr    = [] # french original
        self.frm   = [] # french modified

        for row in reader:
            self.rd.append(int(row[0]))
            self.hd.append(hebrew_date(int(row[1]), int(row[2]), int(row[3])))
            self.ho.append(hebrew_date(int(row[4]), int(row[5]), int(row[6])))
            self.je.append(julian_date(int(row[7]), int(row[8]), int(row[9])))
            self.ge.append(gregorian_date(int(row[10]),
                                          int(row[11]),
                                          int(row[12])))
            self.ae.append(gregorian_date(int(row[13]),
                                          int(row[14]),
                                          int(row[15])))
            self.bd.append(balinese_date(self._toBoolean(row[16]),
                                          int(row[17]),
                                          int(row[18]),
                                          int(row[19]),
                                          int(row[20]),
                                          int(row[21]),
                                          int(row[22]),
                                          int(row[23]),
                                          int(row[24]),
                                          int(row[25])))
            self.pas.append(gregorian_date(int(row[26]),
                                          int(row[27]),
                                          int(row[28])))
            self.par.append(gregorian_date(int(row[29]),
                                          int(row[30]),
                                          int(row[31])))
            self.fr.append(french_date(int(row[32]),
                                       int(row[33]),
                                       int(row[34])))
            self.frm.append(french_date(int(row[35]),
                                        int(row[36]),
                                        int(row[37])))

 
class AppendixCTable3TestCase(AppendixCTable3TestCaseBase,
                               unittest.TestCase):
    def testHebrew(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_hebrew(self.hd[i]), self.rd[i])
            self.assertEqual(hebrew_from_fixed(self.rd[i]), self.hd[i])
            # observational
            self.assertEqual(
                observational_hebrew_from_fixed(self.rd[i]), self.ho[i])
            self.assertEqual(
                fixed_from_observational_hebrew(self.ho[i]), self.rd[i])



    def testEaster(self):
        for i in range(len(self.rd)):
            self.assertEqual(
                 gregorian_from_fixed(orthodox_easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.je[i])
            self.assertEqual(
                 gregorian_from_fixed(alt_orthodox_easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.je[i])
            self.assertEqual(
                 gregorian_from_fixed(easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.ge[i])
            self.assertEqual(
                 gregorian_from_fixed(astronomical_easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.ae[i])


    def testBalinese(self):
        for i in range(len(self.rd)):
            self.assertEqual(bali_pawukon_from_fixed(self.rd[i]), self.bd[i])


    def testPersian(self):
        for i in range(len(self.rd)):
            # persian arithmetic
            self.assertEqual(
                fixed_from_arithmetic_persian(self.par[i]), self.rd[i])
            self.assertEqual(
                arithmetic_persian_from_fixed(self.rd[i]), self.par[i])
            # persian astronomical
            self.assertEqual(persian_from_fixed(self.rd[i]), self.pas[i])
            self.assertEqual(fixed_from_persian(self.pas[i]), self.rd[i])


    #def assertEqual(one, two, msg=""):
    #    print one, two

    def testFrenchRevolutionary(self):
        for i in range(len(self.rd)):
            # french revolutionary original
            self.assertEqual(fixed_from_french(self.fr[i]), self.rd[i])
            self.assertEqual(french_from_fixed(self.rd[i]), self.fr[i])
            # french revolutionary modified
            self.assertEqual(fixed_from_arithmetic_french(self.frm[i]), self.rd[i])
            self.assertEqual(arithmetic_french_from_fixed(self.rd[i]), self.frm[i])


class AppendixCTable4TestCaseBase():

    def _toBoolean(self, c):
        return False if c == 'f' else True

    def setUp(self):
        reader = csv.reader(open("dates4.csv", "rU"),
                            delimiter=',',
                            quoting=csv.QUOTE_NONE)
        self.rd    = []
        self.cd    = [] # chinese date
        self.cn    = [] # chinese day name
        self.ms    = [] # major solar term
        self.ohs   = [] # old hindu solar date
        self.mhs   = [] # modern hindu solar date
        self.ahs   = [] # astronomical hindu solar date
        self.ohl   = [] # old hindu lunar date
        self.mhl   = [] # modern hindu lunar date
        self.ahl   = [] # astronomical hindu lunar date
        self.td    = [] # tibetan date


        for row in reader:
            self.rd.append(int(row[0]))
            self.cd.append(chinese_date(int(row[1]), int(row[2]), int(row[3]),
                                        self._toBoolean(row[4]), int(row[5])))
            self.cn.append([int(row[6]), int(row[7])])
            self.ms.append(float(row[8]))
            self.ohs.append(hindu_solar_date(int(row[9]),
                                             int(row[10]),
                                             int(row[11])))
            self.mhs.append(hindu_solar_date(int(row[12]),
                                             int(row[13]),
                                             int(row[14])))
            self.ahs.append(hindu_solar_date(int(row[15]),
                                             int(row[16]),
                                             int(row[17])))
            self.ohl.append(old_hindu_lunar_date(int(row[18]),
                                             int(row[19]),
                                             self._toBoolean(row[20]),
                                             int(row[21])))
            self.mhl.append(hindu_lunar_date(int(row[22]),
                                             int(row[23]),
                                             self._toBoolean(row[24]),
                                             int(row[25]),
                                             self._toBoolean(row[26])))
            self.ahl.append(hindu_lunar_date(int(row[27]),
                                             int(row[28]),
                                             self._toBoolean(row[29]),
                                             int(row[30]),
                                             self._toBoolean(row[31])))

            self.td.append(tibetan_date(int(row[32]),
                                        int(row[33]),
                                        self._toBoolean(row[34]),
                                        int(row[35]),
                                        self._toBoolean(row[36])))
 
class AppendixCTable4TestCase(AppendixCTable4TestCaseBase,
                               unittest.TestCase):
    def testChinese(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_chinese(self.cd[i]), self.rd[i])
            self.assertEqual(chinese_from_fixed(self.rd[i]), self.cd[i])
            self.assertEqual(chinese_day_name(self.rd[i]), self.cn[i])
            self.assertAlmostEqual(
                major_solar_term_on_or_after(self.rd[i]), self.ms[i], 6)

    def testOldHindu(self):
        for i in range(len(self.rd)):
            # solar
            self.assertEqual(fixed_from_old_hindu_solar(self.ohs[i]), self.rd[i])
            self.assertEqual(old_hindu_solar_from_fixed(self.rd[i]), self.ohs[i])
            # lunisolar
            self.assertEqual(fixed_from_old_hindu_lunar(self.ohl[i]), self.rd[i])
            self.assertEqual(old_hindu_lunar_from_fixed(self.rd[i]), self.ohl[i])


    def testHinduSolarModernToFixed(self):
        for i in range(len(self.rd)):
            # hindu solar
            #    modern
            self.assertEqual(fixed_from_hindu_solar(self.mhs[i]), self.rd[i])

    def testHinduSolarModernFromFixed(self):
        for i in range(len(self.rd)):
            # hindu solar
            #    modern
            self.assertEqual(hindu_solar_from_fixed(self.rd[i]), self.mhs[i])

    def testHinduSolarAstronomicalToFixed(self):
        for i in range(len(self.rd)):
            #    astronomical
            self.assertEqual(fixed_from_astro_hindu_solar(self.ahs[i]), self.rd[i])

    def testHinduSolarAstronomicalFromFixed(self):
        for i in range(len(self.rd)):
            #    astronomical
            self.assertEqual(astro_hindu_solar_from_fixed(self.rd[i]), self.ahs[i])

    def testHinduLunisolarModernToFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    modern
            self.assertEqual(fixed_from_hindu_lunar(self.mhl[i]), self.rd[i])

    def testHinduLunisolarModernFromFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    modern
            self.assertEqual(hindu_lunar_from_fixed(self.rd[i]), self.mhl[i])

    def testHinduLunisolarAstronomicalToFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    astronomical
            self.assertEqual(fixed_from_astro_hindu_lunar(self.ahl[i]), self.rd[i])

    def testHinduLunisolarAstronomicalFromFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    astronomical
            self.assertEqual(astro_hindu_lunar_from_fixed(self.rd[i]), self.ahl[i])

    def testTibetan(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_tibetan(self.td[i]), self.rd[i])
            self.assertEqual(tibetan_from_fixed(self.rd[i]), self.td[i])




class AppendixCTable5TestCaseBase():

    def _toBoolean(self, c):
        return False if c == 'f' else True

    def setUp(self):
        reader = csv.reader(open("dates5.csv", "rU"),
                            delimiter=',',
                            quoting=csv.QUOTE_NONE)
        self.rd    = []
        self.sl    = [] # solar longitude
        self.nse   = [] # next solstice/equinox
        self.ll    = [] # lunar longitude
        self.nnm   = [] # next new moon
        self.dip   = [] # dawn in Paris
        self.sij   = [] # sunset in Jerusalem

        for row in reader:
            self.rd.append(int(row[0]))
            self.sl.append(float(row[1]))
            self.nse.append(float(row[2]))
            self.ll.append(float(row[3]))
            #self.nnm.append(float(row[4])) # read from errata file
            self.dip.append(row[5])
            self.sij.append(row[9])

        reader1 = csv.reader(open("dates5.errata.csv", "rU"),
                            delimiter=',',
                            quoting=csv.QUOTE_NONE)

        for row in reader1:
            self.nnm.append(float(row[1]))

 
class AppendixCTable5TestCase(AppendixCTable5TestCaseBase,
                               unittest.TestCase):
    def testSolarLongitude(self):
        for i in range(len(self.rd)):
            # +0.5 takes into account that the value has to be
            # calculated at 12:00 UTC
            self.assertAlmostEqual(solar_longitude(self.rd[i] + 0.5),
                                   self.sl[i],
                                   6)

    def testNextSolsticeEquinox(self):
        # I run some tests for Gregorian year 1995 about new Moon and
        # start of season against data from HM Observatory...and they
        # are ok
        for i in range(len(self.rd)):
            t = [solar_longitude_after(SPRING, self.rd[i]),
                 solar_longitude_after(SUMMER, self.rd[i]),
                 solar_longitude_after(AUTUMN, self.rd[i]),
                 solar_longitude_after(WINTER, self.rd[i])]
            self.assertAlmostEqual(min(t), self.nse[i], 6)

    def testLunarLongitude(self):
        for i in range(len(self.rd)):
            self.assertAlmostEqual(lunar_longitude(self.rd[i]),
                                   self.ll[i],
                                   6)

    def testNextNewMoon(self):
        for i in range(len(self.rd)):
            self.assertAlmostEqual(new_moon_at_or_after(self.rd[i]),
                                   self.nnm[i],
                                   6)

    def testDawnInParis(self):
        # as clarified by Prof. Reingold in CL it is:
        #    (dawn day paris 18d0)
        # note that d0 stands for double float precision and in
        # the Python routines we use mpf with 52 digits for dawn()
        alpha = angle(18, 0, 0)
        for i in range(len(self.rd)):
            if (self.dip[i] == BOGUS):
                self.assertEqual(dawn(self.rd[i], PARIS, alpha), self.dip[i])
            else:
                self.assertAlmostEqual(
                           mod(dawn(self.rd[i], PARIS, alpha), 1),
                           mpf(self.dip[i]),
                           6)

    def testSunsetInJerusalem(self):
        for i in range(len(self.rd)):
            self.assertAlmostEqual(
                 mod(sunset(self.rd[i], JERUSALEM), 1),
                 float(self.sij[i]),
                 6)




if __name__ == "__main__":
    unittest.main()


