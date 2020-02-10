import React from 'react'
import PropTypes from 'prop-types'
import ReactDOM from 'react-dom'
import Modal from 'react-modal'
import CookieManager from '../../directory_components/static/directory_components/js/dit.components.cookie-notice'

import styles from './CookiesModal.css'

export function CookiesModal(props){
  const [isOpen, setIsOpen] = React.useState(props.isOpen)

  function hanleAcceptAllCookies(event) {
    CookieManager.acceptAllCookiesAndShowSuccess(event)
    setIsOpen(false)
  }

  return (
    <Modal
      isOpen={isOpen}
      contentLabel="Cookies consent manager"
    >
      <h2 className={`${styles.heading} heading-medium`}>Tell us whether you accept cookies</h2>
      <p className={`${styles.synopsis} body-text`} >
        We use <a className="link" href={props.privacyCookiesUrl}>cookies to collect information</a> about how you use great.gov.uk. We use this information to make the website work as well as possible and improve government services.
      </p>
      <div className={styles.buttonContainer}>
        <a className={`${styles.button} button`} href="#" onClick={hanleAcceptAllCookies}>Accept all cookies</a>
        <span className={styles.buttonSeperator}></span>
        <a className={`${styles.button} button`} href={props.preferencesUrl}>Set cookie preferences</a>
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
