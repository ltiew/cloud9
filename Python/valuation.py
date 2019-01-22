"""
Python SDK for F3 Platform: Toy Valuation sample code.

Perform a toy valuation to demonstrate the "laziness" of Python MicroServices.

Try it by running this command in the command prompt:

.. code-block:: bash

    python -m clients.example3_toy_valuation

"""

from datetime import date, timedelta
# Connect to F3 Platform using the location and credentials specified in the configuration module f3sdk.services.config
from f3sdk.f3.singleton import f3
from f3sdk.f3 import repo
# In addition, it is necessary to import "wait", which initiates Platform computations.
# After Platform finishes the computation, results are returned
from f3sdk.lib.coroutine import wait
# The @typechecked decorator will insert a runtime check of the function inputs and of the function result for conformance with type annotations
from f3sdk.lib.typecheck import typechecked
from typing import Union

@typechecked
def toy_valuation(rate: float, maturity: Union[str, date], maturity_convention: str = "NewYorkModFoll") -> float:
    """
    Value a cashflow of one megadollar delivered at the specified maturity.
    The `maturity` can be a specific date or a symbolic specification, such as "3m".
    The `rate` describes the discount curve, with annual compounding, and with time measured by the day count convention act/365f.
    """
    amount = 10**6
    today = date.today()
    maturity_date = f3.MaturityDate(today, maturity, maturity_convention)
    # When we use F3 below to make a product and model, then value the product in that model, the objects returned
    # know how to generate the F3ML that encodes the associated function calls. In addition, all relevant relationships
    # between them are tracked automatically, such that when "wait(f3.evaluate(obj))" is called on any object,
    # the appropriate F3ML document is assembled and run on an F3 Platform calculation worker. This is the sense in which
    # calling F3 is lazy within the SDK.
    product = f3.CreateSingleCashflowProduct(maturity_date, 1, amount, "USD", "Rec")
    # Note: unlike F3 Excel Edition, in Python SDK the object-creating
    # functions do not take the object name input. Object names are auto-generated.
    # If you really need a specific name, you can use the .named method:
    #     product = product.named("my product name")
    model = f3.AddSimpleDiscountCurveToModel(today, rate, "USD")
    # Another way to avoid magic strings of F3 Excel Edition and to benefit from auto-complete functionality of IDEs
    # is using f3sdk.f3.repo module, which defines all repositories and built-in objects of F3 core library.
    result = f3.ValueProduct(model, product, repo.ValuationSpecification.ClosedForm, "Value")
    # No work has been done by Platform yet. The next line is where that happens.
    value = wait(f3.evaluate(result))
    # The simple rule is that no F3 calculations are performed until "wait(f3.evaluate(obj))" is called.

    # value looks like [['USD', 990963.11]], so we index into that list of lists to pick out the numerical value we want.
    # Note that if instead we had said: value = await f3.evaluate(result[0][1]), because our calls to F3 are lazy,
    # we don't have the list of lists to index into. However, objects returned by the F3 SDK support such indexing lazily,
    # meaning that the associated F3ML, when generated, will contain an extra line with the F3 function SubArray that performs
    # the indexing on the return value from F3.
    return value[0][1]

if __name__ == "__main__":
    discount_curve_rate = 0.01
    cashflow_value = toy_valuation(discount_curve_rate, "90d", "NoHolidays")
    print(cashflow_value)
    # because we used the NoHolidays maturity convention, this assertion should hold on any day
    assert round(cashflow_value, 2) == 997549.50
    other_value = toy_valuation(discount_curve_rate, date.today() + timedelta(days=90), "NoHolidays")
    assert cashflow_value == other_value
