from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Tratta:
    airportP : Airport
    airportA : Airport
    peso: int