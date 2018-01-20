import React from 'react'
import ReactDOM from 'react-dom'
import SimpleChartParameter from './SimpleChart'

ReactDOM.render(
    <SimpleChartParameter
      chartType='column'
      renderedSVGClassName='who-cares'
    ></SimpleChartParameter>,
    document.getElementById('root')
);
