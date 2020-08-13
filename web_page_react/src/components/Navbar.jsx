import React from 'react'

export const Navbar = () => {
    return (
        <div>
            <nav className="navbar navbar-dark bg-dark">>
  <a className="navbar-brand" href="https://github.com/emtiyl/meepUnderGraduateResearch">Github Page</a>

    <ul className="navbar-nav mr-auto list-group-horizontal">
      <li className="nav-item mr-2">
        <a className="nav-link" href="https://github.com/emtiyl/meepUnderGraduateResearch/graphs/contributors">Contributers <span className="sr-only">(current)</span></a>
      </li>
      <li className="nav-item">
        <a className="nav-link" href="https://github.com/emtiyl/meepUnderGraduateResearch/blob/master/README.md">ReadMe</a>
      </li>
    </ul>
    <span className="navbar-text">
      Stretching Transmission Spectrum Simulations of Gold with Meep
    </span>

</nav>
        </div>
    )
}
