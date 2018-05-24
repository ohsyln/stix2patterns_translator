from enum import Enum
import typing


class ComparisonComparators(Enum):
    """ Used inside a Comparison Expression to describe a relationship between a field and value. """
    (
        Equal,
        NotEqual,
        GreaterThan,
        LessThan,
        GreaterThanOrEqual,
        LessThanOrEqual,
        In,
        Like,
        Matches,
        IsSubSet,
        IsSuperSet
    ) = range(11)

    def __repr__(self):
        return self._name_

class ComparisonExpressionOperators(Enum):
    """ Used to combine two Comparison Expressions together inside an ObservationExpression"""
    (
        And,
        Or
    ) = range(2)

    def __repr__(self):
        return self._name_


class ObservationOperators(Enum):
    """ Used to combine two or more ObservationExpressions."""
    (
        And,
        Or,
        FollowedBy
    ) = range(3)

    def __repr__(self):
        return self._name_

class Qualifiers(Enum):
    """ various types of qualifiers """
    (
        Repeats,
        Within,
        StartStop
    ) = range(3)
    
    def __repr__(self):
        return self._name_

class Qualifier:
    def __init__(self, type: str, value1: int, value2: int = None) -> None:
        self.type = type
        self.value1 = value1
        self.value2 = value2
        
    def __repr__(self) -> str:
        return "Qualifier({type} {value1} {value2})".format(
            type=self.type, value1=self.value1, value2=self.value2)
    
class QualifierList:
    def __init__(self, new_qualifier: Qualifier) -> None:
        self.qualifiers = [new_qualifier]
       
    def add_qualifier(self, new_qualifier: Qualifier) -> None:
        self.qualifiers.append(new_qualifier)
        
    def __repr__(self) -> str:
        return "QualifierList({qualifiers})".format(qualifiers=self.qualifiers)
    
    
class STIX2Value:
    pass


class SetValue(STIX2Value):
    def __init__(self):
        self.values = []
        self.is_open = True

    def append(self, value):
        if self.is_open:
            self.values.append(value)
        else:
            raise RuntimeError("Cannot append to closed Set")

    def close(self):
        self.is_open = False

    def element_iterator(self):
        for value in self.values:
            yield str(value)

    def __str__(self):
        return "({})".format(str(self.values).lstrip('[').rstrip(']'))


class BaseComparisonExpression:
    pass


class ComparisonExpression(BaseComparisonExpression):
    def __init__(self, object_path, value, comparator: ComparisonComparators, 
                 negated: bool=False, qualifier: QualifierList=None):
        if not isinstance(comparator, ComparisonComparators):
            raise RuntimeWarning("{} is not a ComparisonComparator".format(comparator))
        self.object_path = object_path
        self.value = value
        self.comparator = comparator
        self.negated = negated
        self.qualifiers = qualifiers

    def __repr__(self):
        return "ComparisonExpression({field} {comparator} {value} {qualifiers})".format(comparator=self.comparator,
                                                                           field=self.object_path,
                                                                           value=self.value,
                                                                           qualifiers=self.qualifiers)


class CombinedComparisonExpression(BaseComparisonExpression):
    def __init__(self, expr1: BaseComparisonExpression, expr2: BaseComparisonExpression,
                 operator: ComparisonExpressionOperators, qualifiers: QualifierList=None) -> None:
        if not all((isinstance(expr1, BaseComparisonExpression), isinstance(expr2, BaseComparisonExpression),
                   isinstance(operator, ComparisonExpressionOperators))):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__))
        self.expr1 = expr1
        self.expr2 = expr2
        self.operator = operator
        self.qualifiers = qualifiers

    def __repr__(self) -> str:
        return "CombinedComparisonExpression({expr1} {operator} {expr2} {qualifiers})".format(expr1=self.expr1,
                                                                                 operator=self.operator,
                                                                                 expr2=self.expr2,
                                                                                 qualifiers=self.qualifiers)


class BaseObservationExpression:
    pass

    
class ObservationExpression(BaseObservationExpression):
    def __init__(self, comparison_expression: BaseComparisonExpression, qualifiers: QualifierList = None) -> None:
        if not isinstance(comparison_expression, BaseComparisonExpression):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__))
        self.comparison_expression = comparison_expression
        self.qualifiers = qualifiers

    def __repr__(self) -> str:
        return "ObservationExpression({expr} {qualifiers})".format(expr=self.comparison_expression,
                                                                 qualifiers=self.qualifiers)


class CombinedObservationExpression(BaseObservationExpression):
    def __init__(self, expr1: BaseObservationExpression, expr2: BaseObservationExpression,
                 operator: ObservationOperators, qualifiers: QualifierList = None) -> None:
        if not all((isinstance(expr1, BaseObservationExpression), isinstance(expr2, BaseObservationExpression),
                    isinstance(operator, ObservationOperators))):
            raise RuntimeWarning("{} constructor called with wrong types".format(__class__))
        self.expr1 = expr1
        self.expr2 = expr2
        self.operator = operator
        self.qualifiers = qualifiers

    def __repr__(self) -> str:
        return "CombinedObservationExpression({expr1} {operator} {expr2} {qualifiers})".format(expr1=self.expr1,
                                                                                  operator=self.operator,
                                                                                  expr2=self.expr2,
                                                                                  qualifiers=self.qualifiers)


class Pattern:
    def __init__(self, expression: BaseObservationExpression, qualifier=None) -> None:
        if qualifier:
            raise NotImplementedError
        self.expression = expression

    def __repr__(self) -> str:
        return "Pattern[{expression}]".format(expression=self.expression)
