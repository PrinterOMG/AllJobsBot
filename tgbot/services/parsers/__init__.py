from .freelanceru_parser import FreelanceRuParser
from .kwork_parser import KWorkParser
from .habr_parser import HabrParser
from .weblancer_parser import WeblancerParser


parsers_dict = {
    FreelanceRuParser.marketplace_name: FreelanceRuParser,
    KWorkParser.marketplace_name: KWorkParser,
    HabrParser.marketplace_name: HabrParser,
    # WeblancerParser.marketplace_name: WeblancerParser
}
