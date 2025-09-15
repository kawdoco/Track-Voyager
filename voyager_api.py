from astroquery.jplhorizons import Horizons
from datetime import datetime

class VoyagerAPI:

    Voyager_IDs={'1': '-31', '2': '-32'}

    def __init__(self, voyager="1", observer="@sun"):
        if voyager not in self.Voyager_IDs:
            raise ValueError("Invalid Voyager identifier. Use '1' or '2'.")
        self.voyager = voyager
        self.observer = observer

    def _parae_date(self, date_str):
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
            except:
                raise ValueError("Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
            
    def get_position(self, date_str):
        """
        Returns Voyager's position for a given date.
        """
        date = self._parae_date(date_str)
        obj = Horizons(id=self.Voyager_IDs[self.voyager], location=self.observer, epochs={'start':date, 'stop': date, 'step':"1d"})
        eph = obj.ephemerides()
        #print(eph)
        return eph[0]
    
    def get_range(self, start_date, stop_date, step="1d"):
        """
        Returns Voyager's positions over a date range.
        """
        s = self._parae_date(start_date)
        e = self._parae_date(stop_date)
        obj = Horizons(id=self.Voyager_IDs[self.voyager], location=self.observer, epochs={'start':s, 'stop':e, 'step':step})
        return obj.ephemerides()
    
""" 
if __name__ == "__main__":
    api = VoyagerAPI(voyager="1", observer="@sun")
    print(api.get_position("1980-01-01"))
    print(api.get_range("1980-01-01", "1980-01-10", step="2d"))
"""