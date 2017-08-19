# coding: utf-8


class BaseModel:

    def calc(self, benefit_type, *args, **kwargs):
        raise NotImplemented()

    @property
    def name(self):
        return str(self.__class__.__name__)


class BaseModel1(BaseModel):
    def calc(self, benefit_type, *args, **kwargs):
        assert len(args) >= 3
        a, b, c, *o = args
        return (a + b + c) * benefit_type


class BaseModel2(BaseModel):
    def calc(self, benefit_type, *args, **kwargs):
        assert len(args) >= 3
        a, b, c, *o = args
        return (a + b) * benefit_type


class BaseModel3(BaseModel):
    def calc(self, benefit_type, *args, **kwargs):
        assert len(args) >= 3
        a, b, c, *o = args
        return (b + c) * benefit_type


class BaseModel4(BaseModel):
    def calc(self, benefit_type, *args, **kwargs):
        assert len(args) >= 3
        a, b, c, *o = args
        return a * benefit_type


class BaseModel5(BaseModel):
    def calc(self, benefit_type, *args, **kwargs):
        assert len(args) >= 3
        a, b, c, *o = args
        return b + c


class BaseModel6(BaseModel):
    def calc(self, benefit_type, *args, **kwargs):
        assert len(args) >= 3
        a, b, c, *o = args
        return c * benefit_type


active_models = [
    BaseModel1(),
    BaseModel2(),
    BaseModel3(),
    BaseModel4(),
    BaseModel5(),
    BaseModel6(),
]
