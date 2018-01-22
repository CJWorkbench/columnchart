import React from 'react'
import ReactDOM from 'react-dom'
import SimpleChartParameter from './SimpleChart'

ReactDOM.render(
    <div>
      <SimpleChartParameter
        chartType='column'
        renderedSVGClassName='columnchart-svg'
      ></SimpleChartParameter>
    </div>,
    document.getElementById('root')
);
