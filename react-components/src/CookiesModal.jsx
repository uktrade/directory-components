import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import CookieManager from '../../directory_components/static/directory_components/js/dit.components.cookie-notice'

const styles = {
  h2: {
    margin: 0,
  },
  synopsis: {
    fontSize: 19,
    marginBottom: 45,
    paddingTop: 25,
    textAlign: 'left',
  },
  buttonContainer: {
    display: 'flex',
  },
  button: {
    marginBottom: 15,
    height: 52,
    lineHeight: '2em',
    fontSize: 19,
    cursor: 'pointer',
    width: '50%',
    paddingLeft: 0,
    paddingRight: 0,
  },
  modal: {
    content : {
      background: '#ffffff',
      bottom: 'auto',
      left: '50%',
      marginRight: '-50%',
      paddingLeft: 52,
      paddingRight: 52,
      paddingTop: 54,
      right: 'auto',
      top: '50%',
      transform: 'translate(-50%, -50%)',
      width: 616,
      height: 375,
    },
    overlay: {
      zIndex: 1000,
    },
  },
}

export function CookiesModal(props){
  const [isOpen, setIsOpen] = React.useState(props.isOpen)

  function hanleAcceptAllCookies(event) {
    CookieManager.acceptAllCookiesAndShowSuccess(event)
    setIsOpen(false)
  }

  return (
    <Modal
      isOpen={isOpen}
      style={styles.modal}
      contentLabel="Cookies consent manager"
    >
      <h2 className="heading-medium" style={styles.h2}>Tell us whether you accept cookies</h2>
      <p className="body-text" style={styles.synopsis}>
        We use <a class="link" href={props.privacyCookiesUrl}>cookies to collect information</a> about how you use great.gov.uk. We use this information to make the website work as well as possible and improve government services.
      </p>
      <div style={styles.buttonContainer}>
        <a className="button" style={styles.button} href="#" onClick={hanleAcceptAllCookies}>Accept all cookies</a>
        <span style={{width: 20}}></span>
        <a className="button" style={styles.button} href={props.preferencesUrl}>Set cookie preferneces</a>
      </div>
    </Modal>
  )
}

CookiesModal.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  preferencesUrl: PropTypes.string.isRequired,
}

export default function createCookiesModal({ element, ...params }) {
  Modal.setAppElement(element)
  ReactDOM.render(<CookiesModal {...params} />, element)
}
