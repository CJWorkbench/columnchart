import React from 'react'
import ReactDOM from 'react-dom'
import SimpleChartParameter from './SimpleChart'

ReactDOM.render(
    <SimpleChartParameter
      wf_module_id={workbench.data.wfmodule.id}
      revision={workbench.data.workflow}
      chartType='column'
      renderedSVGClassName='who-cares'
    ></SimpleChartParameter>,
    document.getElementById('root')
);
