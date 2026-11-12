Demand
======

The following demand tutorials are available:

* :doc:`A. Define a collective heating demand cluster <../step_by_step/demand/demand_step_a>`

  The total heating demand for a large number of nearby consumers can be aggregated and
  represented by a collective heating demand cluster.

  This can be a useful method for the draft design of an integral heating system (i.e.
  from source up to consumers), as it avoids drawing every pipe line connecting to each
  individual consumer and also speeds up calculations.

  In this Step by step, we explain how to apply this method for 4th generation heating
  networks, where the primary and secondary grids (the distribution grid) are separate
  hydraulical systems that connect at the so-called heating transfer substations

  Nonetheless, the designer can also define collective heating demand clusters that
  aggregate demand at another spatial level, for instance for a street, a municipality
  or a region, depending on the system scale and design exercise at hand.

* :doc:`B. Account for changes in collective heating demand clusters during the heating transition <../step_by_step/demand/demand_step_b>`

  The collective heating demand cluster we just defined will transform during the
  heating transition.

  That means we need to account for various changes we know or expect to occur in the
  clusters, e.g. insulation of dwellings and buildings, demolition or (re)construction
  of neighbourhoods, effects of climate change and different consumer behaviour w.r.t.
  heating demand.

  These changes are effectuated in the properties of the collective heating demand
  cluster, e.g. the demand area for which demand is aggregated, associated heating
  demand profile and costs.

  And they should be pinned to a timeline the future moments we expect the changes to
  occur.

  For this, we use the scenario manager.
